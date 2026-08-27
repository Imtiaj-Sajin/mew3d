"""LightSmith: designs a studio lighting rig that flatters a specific model.

The rig is deliberately renderer-agnostic - a background gradient plus a few coloured
lights placed by azimuth/elevation. The web UI paints it into an equirectangular
environment map, so the same description drives image-based lighting in the viewer.

Runs on demand from the studio UI (after a model is on screen) rather than inside the
generation pipeline, so relighting never blocks the GPU work.
"""

LIGHTING_SYSTEM = """You are the lighting director of a 3D studio. Given a subject (and a
render of it) design a lighting rig that makes it look striking and professional - the way
a product photographer or a game's key art would light it. Think about the subject's
material and mood: chrome and car paint want bright rim separation and a dark backdrop;
creatures want warm key light with cool rim; food wants soft warm light on a bright ground.

Angles: azimuth 0 is in front of the model, 90 is its right, 180 behind, -90 its left.
Elevation 0 is level with the model, 90 straight above, negative from below.

Reply with JSON only:
{"preset_name": "<2-3 word name for this look>",
 "background": {"top": "#rrggbb", "bottom": "#rrggbb"},
 "lights": [
   {"role": "key",  "color": "#rrggbb", "azimuth": <-180..180>, "elevation": <-30..90>,
    "intensity": <0.2..1.5>, "size": <0.1..0.6>},
   {"role": "fill", "color": "#rrggbb", "azimuth": ..., "elevation": ..., "intensity": ..., "size": ...},
   {"role": "rim",  "color": "#rrggbb", "azimuth": ..., "elevation": ..., "intensity": ..., "size": ...}
 ],
 "exposure": <0.6..1.6>,
 "shadow_intensity": <0..1.5>,
 "rationale": "<one sentence: why this lighting suits THIS subject>",
 "commentary": ["<short line about the key light>", "<short line about the rim/fill>"]}
Use exactly three lights: key, fill, rim. `size` is the softness of the source."""


# Fallback rigs, used when no LLM is reachable. Keyed by the Analyst's category.
PRESETS = {
    "vehicle": {
        "preset_name": "Neon Showroom",
        "background": {"top": "#141a24", "bottom": "#05070b"},
        "lights": [
            {"role": "key", "color": "#ffffff", "azimuth": 35, "elevation": 40,
             "intensity": 1.2, "size": 0.30},
            {"role": "fill", "color": "#3f6fff", "azimuth": -75, "elevation": 10,
             "intensity": 0.5, "size": 0.55},
            {"role": "rim", "color": "#c8ff3f", "azimuth": 165, "elevation": 25,
             "intensity": 1.0, "size": 0.22},
        ],
        "exposure": 1.1, "shadow_intensity": 1.0,
        "rationale": "Hard key with a coloured rim reads the panel creases and gives "
                     "glossy paint something to reflect.",
        "commentary": ["Tight key light at 35 degrees to catch the bodywork highlights.",
                       "Lime rim from behind separates the silhouette from the dark set."],
    },
    "creature": {
        "preset_name": "Warm Character Key",
        "background": {"top": "#232028", "bottom": "#0b0a0d"},
        "lights": [
            {"role": "key", "color": "#ffd9a8", "azimuth": 30, "elevation": 35,
             "intensity": 1.1, "size": 0.38},
            {"role": "fill", "color": "#7fa8ff", "azimuth": -60, "elevation": 5,
             "intensity": 0.45, "size": 0.6},
            {"role": "rim", "color": "#bfd8ff", "azimuth": 175, "elevation": 40,
             "intensity": 0.8, "size": 0.3},
        ],
        "exposure": 1.0, "shadow_intensity": 0.9,
        "rationale": "A warm key with cool fill keeps skin and scales readable while the "
                     "rim lifts the subject off the background.",
        "commentary": ["Warm key from the upper right shapes the face and limbs.",
                       "Cool fill and a bright rim stop the dark areas going flat."],
    },
    "food": {
        "preset_name": "Fresh Daylight",
        "background": {"top": "#f2efe6", "bottom": "#cfc8ba"},
        "lights": [
            {"role": "key", "color": "#fff4e0", "azimuth": 25, "elevation": 50,
             "intensity": 1.15, "size": 0.5},
            {"role": "fill", "color": "#ffffff", "azimuth": -70, "elevation": 15,
             "intensity": 0.6, "size": 0.6},
            {"role": "rim", "color": "#ffe9c9", "azimuth": 160, "elevation": 30,
             "intensity": 0.5, "size": 0.4},
        ],
        "exposure": 1.2, "shadow_intensity": 0.6,
        "rationale": "Soft bright daylight keeps food appetising and avoids harsh shadows.",
        "commentary": ["Broad soft key mimics window light.",
                       "Bright surroundings keep the shadows open and fresh."],
    },
    "default": {
        "preset_name": "Neutral Studio",
        "background": {"top": "#2a2d33", "bottom": "#0d0f12"},
        "lights": [
            {"role": "key", "color": "#ffffff", "azimuth": 30, "elevation": 35,
             "intensity": 1.0, "size": 0.4},
            {"role": "fill", "color": "#cfd8e8", "azimuth": -65, "elevation": 10,
             "intensity": 0.5, "size": 0.6},
            {"role": "rim", "color": "#ffffff", "azimuth": 170, "elevation": 30,
             "intensity": 0.7, "size": 0.3},
        ],
        "exposure": 1.0, "shadow_intensity": 0.9,
        "rationale": "A classic three-point studio setup that reads shape cleanly.",
        "commentary": ["Standard three-point rig: key, fill, rim.",
                       "Neutral colours so the model's own materials lead."],
    },
}

_ALIASES = {
    "character": "creature", "prop": "default", "furniture": "default",
    "architecture": "default", "abstract": "default", "other": "default",
}

_HEX = "0123456789abcdefABCDEF"


def _valid_hex(value) -> bool:
    return (isinstance(value, str) and len(value) == 7 and value[0] == "#"
            and all(c in _HEX for c in value[1:]))


def _clamp(value, low, high, fallback):
    try:
        return max(low, min(high, float(value)))
    except (TypeError, ValueError):
        return fallback


def fallback_rig(category: str | None) -> dict:
    key = (category or "default").lower()
    return PRESETS[_ALIASES.get(key, key if key in PRESETS else "default")]


def sanitise(rig: dict, category: str | None) -> dict | None:
    """Coerce an LLM rig into safe ranges; None if it is unusable."""
    base = fallback_rig(category)
    if not isinstance(rig, dict) or not isinstance(rig.get("lights"), list):
        return None

    lights = []
    for want, spec in zip(("key", "fill", "rim"), rig["lights"]):
        if not isinstance(spec, dict):
            continue
        default = next(x for x in base["lights"] if x["role"] == want)
        color = spec.get("color")
        lights.append({
            "role": want,
            "color": color if _valid_hex(color) else default["color"],
            "azimuth": _clamp(spec.get("azimuth"), -180, 180, default["azimuth"]),
            "elevation": _clamp(spec.get("elevation"), -30, 90, default["elevation"]),
            "intensity": _clamp(spec.get("intensity"), 0.0, 1.5, default["intensity"]),
            "size": _clamp(spec.get("size"), 0.08, 0.7, default["size"]),
        })
    if len(lights) != 3:
        return None

    bg = rig.get("background") if isinstance(rig.get("background"), dict) else {}
    commentary = [str(c)[:160] for c in rig.get("commentary", [])
                  if isinstance(c, (str, int, float))][:3]
    return {
        "preset_name": str(rig.get("preset_name") or base["preset_name"])[:40],
        "background": {
            "top": bg.get("top") if _valid_hex(bg.get("top")) else base["background"]["top"],
            "bottom": (bg.get("bottom") if _valid_hex(bg.get("bottom"))
                       else base["background"]["bottom"]),
        },
        "lights": lights,
        "exposure": _clamp(rig.get("exposure"), 0.4, 2.0, base["exposure"]),
        "shadow_intensity": _clamp(rig.get("shadow_intensity"), 0.0, 1.5,
                                   base["shadow_intensity"]),
        "rationale": str(rig.get("rationale") or base["rationale"])[:300],
        "commentary": commentary or base["commentary"],
    }


def design_lighting(llm, subject: str, category: str | None, preview_path=None) -> dict:
    """Ask the vision LLM for a rig for this model; fall back to a preset."""
    prompt = (f"Subject: {subject!r} (category: {category or 'unknown'}). "
              "Design the lighting rig that best presents this model.")
    raw = None
    if getattr(llm, "usable", False):
        if preview_path:
            raw = llm.chat_json_vision("LightSmith", LIGHTING_SYSTEM, prompt, preview_path)
        else:
            raw = llm.chat_json("LightSmith", LIGHTING_SYSTEM, prompt)

    rig = sanitise(raw, category) if raw else None
    if rig:
        rig["source"] = "ai"
        return rig
    rig = dict(fallback_rig(category))
    rig["source"] = "preset"
    return rig


DEFAULT_RIG = dict(PRESETS["default"], source="default", preset_name="Default Viewer")
