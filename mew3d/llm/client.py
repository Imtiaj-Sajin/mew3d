"""OpenAI-compatible LLM client with a circuit breaker.

The whole pipeline must work with NO working key (heuristic fallbacks in every agent),
and get smarter automatically when a real key lands in .env.
"""

import json
import os
import re


class LLMClient:
    def __init__(self, bus, enabled: bool = True) -> None:
        self.bus = bus
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        api_key = os.getenv("OPENAI_API_KEY", "").strip().strip('"')
        # explicit default: an empty OPENAI_BASE_URL env var would otherwise be used
        # verbatim by the openai client, producing protocol-less request URLs
        base_url = (
            os.getenv("OPENAI_BASE_URL", "").strip().strip('"')
            or "https://api.openai.com/v1"
        )
        self.available = enabled and bool(api_key)
        self._tripped = False
        self._client = None
        if self.available:
            try:
                from openai import OpenAI

                self._client = OpenAI(
                    api_key=api_key, base_url=base_url, timeout=45.0, max_retries=1
                )
            except Exception as e:
                self.bus.emit("llm", "log", f"LLM client init failed, using heuristics: {e}")
                self.available = False

    @property
    def usable(self) -> bool:
        return self.available and not self._tripped

    def chat(self, agent: str, system: str, user: str) -> str | None:
        """Returns the reply text, or None (caller must fall back to heuristics)."""
        if not self.usable:
            return None
        try:
            resp = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=0.7,
                max_tokens=700,
            )
            text = resp.choices[0].message.content
            self.bus.emit(agent, "log", "LLM responded", model=self.model)
            return text
        except Exception as e:
            self._tripped = True  # don't stall every later agent on a dead endpoint
            self.bus.emit(
                "llm", "log",
                f"LLM unavailable ({type(e).__name__}), all agents switching to heuristic mode",
            )
            return None

    def chat_vision(self, agent: str, system: str, user: str, image_path) -> str | None:
        """Chat about an image (base64-inlined, low detail); None on any failure."""
        if not self.usable:
            return None
        import base64
        from pathlib import Path

        try:
            b64 = base64.b64encode(Path(image_path).read_bytes()).decode()
            resp = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{b64}",
                                    "detail": "low",
                                },
                            },
                        ],
                    },
                ],
                temperature=0.2,
                max_tokens=400,
            )
            text = resp.choices[0].message.content
            self.bus.emit(agent, "log", "vision LLM responded", model=self.model)
            return text
        except Exception as e:
            self._tripped = True
            self.bus.emit(
                "llm", "log",
                f"vision LLM unavailable ({type(e).__name__}), switching to heuristics",
            )
            return None

    def chat_json_vision(self, agent: str, system: str, user: str, image_path) -> dict | None:
        text = self.chat_vision(
            agent, system + " Respond with a single JSON object only.", user, image_path
        )
        return self._parse_json(text)

    def chat_json(self, agent: str, system: str, user: str) -> dict | None:
        """Chat and parse a JSON object out of the reply; None on any failure."""
        text = self.chat(agent, system + " Respond with a single JSON object only.", user)
        return self._parse_json(text)

    @staticmethod
    def _parse_json(text: str | None) -> dict | None:
        if not text:
            return None
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return None
        try:
            parsed = json.loads(match.group(0))
            return parsed if isinstance(parsed, dict) else None
        except json.JSONDecodeError:
            return None


VISION_CANDIDATE_SYSTEM = """You are the vision critic of a 3D-generation studio. The image
you receive will be fed to a single-image 3D reconstruction model. Judge it strictly:
{"complete_object": <true only if the ENTIRE object is inside the frame, nothing cut off
 by any edge>,
 "single_object": <true if there is exactly one main object>,
 "matches_subject": <true if it clearly depicts the requested subject>,
 "clean_background": <true if the background is plain and uncluttered>,
 "score": <0-10 overall suitability for 3D reconstruction>,
 "issue": "<the single biggest problem, or 'none'>"}"""

VISION_MESH_SYSTEM = """You are the quality judge of a 3D-generation studio. The image is a
rendered view of a reconstructed 3D model. Judge whether the reconstruction succeeded:
{"looks_like_subject": <true if the render clearly shows the requested subject in 3D>,
 "is_flat_or_blob": <true if it looks like a flat slab, billboard, or shapeless blob>,
 "score": <0-10 quality of the 3D shape>,
 "issue": "<the single biggest problem, or 'none'>"}"""
