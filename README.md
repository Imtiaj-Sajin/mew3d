# Mew3D — Local Agentic Text/Image → 3D Studio

Turn **text**, an **image**, or **both** into a 3D model (OBJ + GLB), fully local on an
RTX 3060 Ti (8GB), coordinated by a crew of AI agents with live progress and full run logs.

<img width="1919" height="944" alt="image" src="https://github.com/user-attachments/assets/8dc9e1cb-45a0-4725-acdf-2a9fd833e400" />


## Setup on a new PC

```powershell
git clone https://github.com/Imtiaj-Sajin/mew3d.git
cd mew3d
powershell -ExecutionPolicy Bypass -File setup.ps1   # venv + deps + models (~7GB total)
# then put your OPENAI_API_KEY into .env (copied from .env.example automatically)
```

Requirements: Python 3.11+, NVIDIA GPU with 6GB+ VRAM (tested on RTX 3060 Ti 8GB).
Models cache into `models/` inside the repo folder; `.env`, `models/`, and `results/`
stay local and are never pushed.

## Quick start

```powershell
.venv\Scripts\python.exe -m mew3d doctor                       # environment check
.venv\Scripts\python.exe -m mew3d generate --text "a cute dragon"
.venv\Scripts\python.exe -m mew3d generate --image photo.jpg
.venv\Scripts\python.exe -m mew3d generate --image photo.jpg --text "a wooden chair"
```

To run the frontend with auto backend start:
```powershell
 .venv\Scripts\python.exe -m mew3d serve

```

First run downloads models (~7GB total) into `models/` on this drive.

## The agent crew

| Agent | Role |
|---|---|
| 🧠 Orchestrator | central agent: routes work, runs the judge/retry loop |
| 🔎 Analyst | judges the request, plans the pipeline, flags multi-object scenes |
| ✍️ PromptSmith | rewrites your text into a 3D-reconstruction-friendly image prompt (LLM, heuristic fallback) |
| 🎨 ImageGen | SD-Turbo / SDXL-Turbo → N candidate images |
| 🪄 Preprocessor | background removal (u2net), scores + selects the best candidate, frames the object |
| 🧊 MeshGen | TripoSR single-image 3D reconstruction + NeRF turntable previews |
| ⚖️ Judge | scores the mesh (fragmentation, face count, shape); orders retries with adjusted parameters |
| 📦 Exporter | writes OBJ/GLB + `report.md` |

Pipelines:

```
text:  Analyst → PromptSmith → ImageGen ─┐
image: Analyst ──────────────────────────┴→ Preprocessor → MeshGen → Judge ─(retry?)→ Exporter
```

The Judge can send the pipeline back: pick the next-best candidate image, regenerate with a
new seed, zoom the framing out, or raise marching-cubes resolution — up to `--retries` times.

## Every run is fully recorded

```
results/<timestamp>_<name>/
├─ report.md              # human-readable summary + agent timeline
├─ input/                 # your original image (if any)
├─ intermediate/          # candidate images, bg-removed + framed input
├─ output/                # mesh.obj, mesh.glb, preview_*.png, turntable.gif
└─ logs/
   ├─ events.jsonl        # every agent action, timestamped, machine-readable
   ├─ run.log             # plain-text log
   ├─ analysis.json, prompt.json, judge_attempt_*.json
```

## 3D backends

| backend | quality | speed | output |
|---|---|---|---|
| `--mesh-model triposr` (default) | okay, bumpy | ~15s | vertex-colored |
| `--mesh-model hunyuan` | much better geometry | ~45s | untextured (clay) |
| `--mesh-model both` | runs BOTH on the same input | ~60s | side-by-side, judge picks winner |

Hunyuan3D-2mini needs ~5GB VRAM (fits 8GB cards); its texture stage needs 16GB so we
run shape-only. In compare mode both meshes land in `output/` as `triposr_mesh.glb` /
`hunyuan_mesh.glb` with a comparison table in `report.md`.

## Useful flags

`--candidates 4` more images to choose from · `--image-model sdxl-turbo` higher quality, slower ·
`--mc-res 320` finer mesh · `--retries 2` more judge retries · `--no-llm` heuristics only ·
`--plain` plain logs instead of the live dashboard · `--seed 42` reproducible

## LLM

Agents use the OpenAI-compatible key in `.env` for analysis, prompt enhancement, and judging
second opinions. **Everything works without it** — agents detect a dead key once and switch to
heuristic mode for the rest of the run.

## Notes

- VRAM is managed: only one heavy model (image gen OR TripoSR) is resident at a time.
- TripoSR is vendored in `third_party/TripoSR` with `torchmcubes` swapped for scikit-image
  marching cubes (no C++/CUDA compilation needed on Windows).
- View `mesh.glb` in Windows 3D Viewer, https://gltf-viewer.donmccurdy.com/, or Blender.
