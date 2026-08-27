"""Mew3D web server: FastAPI backend for the studio UI.

- POST /api/generate       start a run (text and/or image); one at a time (GPU)
- GET  /api/status         is the pipeline busy
- GET  /api/runs           all runs with their outputs/scores
- GET  /api/runs/{id}/events?after=N   incremental agent-event feed
- /files/*                 results folder (GLBs, previews)
- /                        the studio UI

A Narrator agent (Groq, free tier) turns pipeline events into friendly commentary,
and a guardrail check screens text prompts before the GPU spins up.
"""

import json
import os
import queue
import threading
import time
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from .config import RESULTS_DIR, GenerationConfig, PROJECT_ROOT, setup_environment

setup_environment()

app = FastAPI(title="Mew3D")

# Optional shared-password gate. Unset (the default) means no auth, which is fine on
# localhost; `serve --public` refuses to open a tunnel unless this is set.
ACCESS_TOKEN = (os.getenv("MEW3D_ACCESS_TOKEN") or "").strip().strip('"')
_COOKIE = "mew3d_key"

_LOGIN_PAGE = """<!doctype html><meta charset=utf-8><title>Mew3D</title>
<style>body{background:#0d1117;color:#e6edf3;font:15px system-ui;display:grid;
place-items:center;height:100vh;margin:0}form{background:#161b22;border:1px solid #2d333b;
padding:28px;border-radius:12px;display:flex;flex-direction:column;gap:12px;width:280px}
input{padding:10px;border-radius:8px;border:1px solid #2d333b;background:#1c2330;color:#e6edf3}
button{padding:10px;border:0;border-radius:8px;background:#58a6ff;color:#fff;font-weight:600;
cursor:pointer}h1{font-size:18px;margin:0 0 4px}</style>
<form method=get action=/><h1>Mew<span style=color:#58a6ff>3D</span> Studio</h1>
<input name=k type=password placeholder="access key" autofocus>
<button>Enter</button>__MSG__</form>"""


@app.middleware("http")
async def _gate(request: Request, call_next):
    if not ACCESS_TOKEN:
        return await call_next(request)
    supplied = request.query_params.get("k") or request.cookies.get(_COOKIE) or ""
    if supplied == ACCESS_TOKEN:
        response = await call_next(request)
        if request.query_params.get("k"):
            response.set_cookie(_COOKIE, ACCESS_TOKEN, max_age=604800, samesite="lax")
        return response
    if request.url.path.startswith("/api/"):
        return HTMLResponse('{"detail":"unauthorized"}', status_code=401,
                            media_type="application/json")
    wrong = request.query_params.get("k") is not None
    return HTMLResponse(
        _LOGIN_PAGE.replace(
            "__MSG__", "<span style=color:#f85149>wrong key</span>" if wrong else ""
        ),
        status_code=401,
    )

_busy = threading.Lock()
_current_run: dict = {"run_id": None}
UPLOADS_DIR = PROJECT_ROOT / "uploads"

STATIC_DIR = Path(__file__).parent / "ui" / "static"


# ---------------------------------------------------------------- Groq helpers
def _groq_client():
    key = (os.getenv("GROQ_API_KEY") or "").strip().strip('"')
    if not key:
        return None
    from openai import OpenAI

    return OpenAI(api_key=key, base_url="https://api.groq.com/openai/v1",
                  timeout=25, max_retries=0)


def groq_chat(system: str, user: str, max_tokens: int = 350) -> str | None:
    client = _groq_client()
    if client is None:
        return None
    try:
        resp = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b").strip('"'),
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
            temperature=0.7,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content
    except Exception:
        return None


GUARD_SYSTEM = """You are the content guardrail of a 3D-object generator. Judge whether a
prompt is acceptable to turn into a 3D model. Reject sexual content involving minors,
realistic depictions of real living people, hate symbols, and instructions for weapons.
Ordinary creatures, characters, props, vehicles, food, fantasy weapons for games etc. are
all fine. Reply ONLY with JSON: {"allowed": true/false, "reason": "<short>"}"""


def guardrail_check(text: str) -> tuple[bool, str]:
    """Fail-open: if the guardrail LLM is unreachable, allow and note it."""
    reply = groq_chat(GUARD_SYSTEM, f"Prompt: {text!r}", max_tokens=100)
    if not reply:
        return True, "guardrail offline - allowed by default"
    try:
        import re

        verdict = json.loads(re.search(r"\{.*\}", reply, re.DOTALL).group(0))
        return bool(verdict.get("allowed", True)), verdict.get("reason", "")
    except Exception:
        return True, "guardrail reply unparseable - allowed by default"


NARRATOR_SYSTEM = """You are the Narrator of Mew3D, a local AI studio where a crew of agents
(Analyst, PromptSmith, ImageGen, Preprocessor, MeshGen, Judge, TextureSmith, Exporter)
collaborate to turn text or an image into a 3D model. You receive a batch of raw pipeline
events. In 1-3 short, warm, plain-English sentences, tell the viewer what the crew just did
and why it matters. Teach a little (one interesting fact max), never repeat earlier
commentary, no emoji spam, no markdown."""


class Narrator:
    """Consumes pipeline events, emits friendly 'Narrator' commentary via Groq."""

    def __init__(self, bus) -> None:
        self.bus = bus
        self.q: queue.Queue = queue.Queue()
        self._stop = threading.Event()
        self._history: list[str] = []
        bus.subscribe(self._on_event)
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def _on_event(self, ev) -> None:
        if ev.agent in ("Narrator", "vram", "llm"):
            return
        if ev.type in ("status", "decision", "artifact", "error"):
            self.q.put(f"{ev.agent} [{ev.type}] {ev.message}")

    def _loop(self) -> None:
        while not self._stop.is_set():
            batch = []
            try:
                batch.append(self.q.get(timeout=2.5))
            except queue.Empty:
                continue
            time.sleep(1.5)  # let a few related events accumulate
            while not self.q.empty() and len(batch) < 12:
                batch.append(self.q.get_nowait())
            context = "\n".join(self._history[-3:])
            text = groq_chat(
                NARRATOR_SYSTEM,
                (f"Your recent commentary (do not repeat):\n{context}\n\n" if context else "")
                + "New events:\n" + "\n".join(batch),
            )
            if text:
                text = text.strip()
                self._history.append(text)
                self.bus.emit("Narrator", "narration", text)

    def stop(self) -> None:
        self._stop.set()


# ---------------------------------------------------------------- run pipeline
def _pipeline_thread(ctx) -> None:
    from .core.orchestrator import Orchestrator

    narrator = Narrator(ctx.bus)
    try:
        Orchestrator(ctx).run()
    except Exception as e:
        ctx.bus.emit("Orchestrator", "error", f"run failed: {type(e).__name__}: {e}")
    finally:
        narrator.stop()
        ctx.close()
        _current_run["run_id"] = None
        _busy.release()


@app.post("/api/generate")
async def generate(
    text: str = Form(None),
    mesh_model: str = Form("hunyuan"),
    texture: bool = Form(True),
    candidates: int = Form(3),
    image: UploadFile = File(None),
):
    if not text and image is None:
        raise HTTPException(400, "provide a text prompt and/or an image")
    if mesh_model not in ("triposr", "hunyuan", "both"):
        raise HTTPException(400, f"unknown mesh_model {mesh_model!r}")
    if not _busy.acquire(blocking=False):
        raise HTTPException(409, "a generation is already running - one at a time on this GPU")

    try:
        image_path = None
        if image is not None:
            UPLOADS_DIR.mkdir(exist_ok=True)
            suffix = Path(image.filename or "upload.png").suffix or ".png"
            image_path = UPLOADS_DIR / f"upload_{int(time.time())}{suffix}"
            image_path.write_bytes(await image.read())

        if text:
            allowed, reason = guardrail_check(text)
            if not allowed:
                raise HTTPException(422, f"prompt rejected by guardrail: {reason}")

        cfg = GenerationConfig(
            text=text or None,
            image=str(image_path) if image_path else None,
            mesh_model=mesh_model,
            texture=texture,
            num_candidates=max(1, min(4, candidates)),
            plain_ui=True,
        )
        from .core.run_context import RunContext

        ctx = RunContext(cfg)
        _current_run["run_id"] = ctx.run_id
        threading.Thread(target=_pipeline_thread, args=(ctx,), daemon=True).start()
        return {"run_id": ctx.run_id}
    except HTTPException:
        _busy.release()
        raise
    except Exception:
        _busy.release()
        raise


@app.get("/api/status")
def status():
    return {"busy": _busy.locked(), "run_id": _current_run["run_id"]}


OUTPUT_LABELS = {
    "mesh.glb": "Mesh",
    "triposr_mesh.glb": "TripoSR",
    "hunyuan_mesh.glb": "Hunyuan",
    "mesh_textured.glb": "Textured",
}


def _run_summary(run_dir: Path) -> dict:
    out = run_dir / "output"
    glbs = sorted(out.glob("*.glb")) if out.is_dir() else []
    previews = sorted(out.glob("*preview*.png"))[:6] if out.is_dir() else []
    score, backend = None, None
    judge_files = sorted(run_dir.glob("logs/judge_attempt_*.json"))
    if judge_files:
        try:
            verdict = json.loads(judge_files[-1].read_text(encoding="utf-8"))
            score, backend = verdict.get("score"), verdict.get("backend")
        except Exception:
            pass
    running = _current_run["run_id"] == run_dir.name
    return {
        "run_id": run_dir.name,
        "mtime": run_dir.stat().st_mtime,
        "score": score,
        "backend": backend,
        "status": "running" if running else ("done" if glbs else "failed"),
        "models": [
            {"label": OUTPUT_LABELS.get(p.name, p.stem), "file": f"/files/{run_dir.name}/output/{p.name}"}
            for p in glbs
        ],
        "previews": [f"/files/{run_dir.name}/output/{p.name}" for p in previews],
    }


@app.get("/api/runs")
def runs(limit: int = 30):
    dirs = sorted(
        (d for d in RESULTS_DIR.iterdir() if d.is_dir()),
        key=lambda d: d.stat().st_mtime, reverse=True,
    )
    return {"runs": [_run_summary(d) for d in dirs[:limit]]}


@app.get("/api/runs/{run_id}/events")
def run_events(run_id: str, after: int = 0):
    if "/" in run_id or "\\" in run_id or ".." in run_id:
        raise HTTPException(400, "bad run id")
    events_file = RESULTS_DIR / run_id / "logs" / "events.jsonl"
    if not events_file.is_file():
        raise HTTPException(404, "run not found")
    events = []
    with open(events_file, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i < after:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    done = _current_run["run_id"] != run_id
    return {"events": events, "next": after + len(events), "done": done}


app.mount("/files", StaticFiles(directory=str(RESULTS_DIR)), name="files")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


def _start_tunnel(port: int) -> None:
    """Open a Cloudflare quick tunnel and print the public URL once it appears."""
    import re
    import subprocess
    import threading

    exe = PROJECT_ROOT / "tools" / "cloudflared.exe"
    if not exe.is_file():
        raise SystemExit(f"cloudflared not found at {exe}")

    proc = subprocess.Popen(
        [str(exe), "tunnel", "--url", f"http://127.0.0.1:{port}", "--no-autoupdate"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        encoding="utf-8", errors="replace",
    )

    def watch():
        for line in proc.stdout:
            found = re.search(r"https://[\w-]+\.trycloudflare\.com", line)
            if found:
                print(f"\n  PUBLIC URL: {found.group(0)}/?k={ACCESS_TOKEN}\n"
                      f"  anyone with this link can use your GPU - share carefully\n",
                      flush=True)

    threading.Thread(target=watch, daemon=True).start()


def main(host: str = "127.0.0.1", port: int = 7860, public: bool = False) -> None:
    import uvicorn

    RESULTS_DIR.mkdir(exist_ok=True)
    if public:
        if not ACCESS_TOKEN:
            raise SystemExit(
                "refusing to expose an unauthenticated server.\n"
                "add MEW3D_ACCESS_TOKEN=\"<a strong passphrase>\" to .env first."
            )
        host = "127.0.0.1"  # the tunnel dials out locally; never bind to 0.0.0.0
        _start_tunnel(port)
    print(f"\n  Mew3D studio: http://{host}:{port}\n")
    uvicorn.run(app, host=host, port=port, log_level="warning")
