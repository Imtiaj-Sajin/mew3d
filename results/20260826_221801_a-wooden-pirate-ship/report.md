# Mew3D Run Report - 20260826_221801_a-wooden-pirate-ship

- **Date:** 2026-08-26 22:19:12
- **Mode:** text23d
- **Text input:** a wooden pirate ship
- **Analyst read:** pirate ship (vehicle, complexity medium)

## Prompt enhancement
- Original: `a wooden pirate ship`
- Enhanced: `full view of a whole wooden pirate ship, centered in 3/4 view against a plain uncluttered background with even studio lighting`
- Negative: `close-up, macro, cropped, text, watermarks`
- Selected candidate: `G:\codes\mew3d\results\20260826_221801_a-wooden-pirate-ship\intermediate\candidate_02_seed689039460.png`

## Quality verdict
- **Score:** 0.84 (PASS)
- Attempts: 1
- Faces: 111,438 | Vertices: 55,733 | Watertight: True | Components: 17
- Attempt 1 LLM opinion: The mesh quality is acceptable but requires attention due to the presence of degenerate faces and multiple components.

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `22:18:02` **Analyst** [status] started
- `22:18:05` **Analyst** [decision] subject 'pirate ship' (vehicle, complexity medium) - Ensure to capture the intricate details of the ship's wood texture and sails.
- `22:18:05` **Analyst** [decision] pipeline plan: PromptSmith -> ImageGen -> Preprocessor -> MeshGen -> Judge -> Exporter
- `22:18:05` **Analyst** [status] done
- `22:18:05` **PromptSmith** [status] started
- `22:18:07` **PromptSmith** [decision] LLM-enhanced prompt: 'full view of a whole wooden pirate ship, centered in 3/4 view against a plain uncluttered background with even studio lighting'
- `22:18:07` **PromptSmith** [status] done
- `22:18:07` **ImageGen** [status] started
- `22:18:43` **ImageGen** [artifact] candidate 1 saved
- `22:18:43` **ImageGen** [artifact] candidate 2 saved
- `22:18:43` **ImageGen** [artifact] candidate 3 saved
- `22:18:43` **ImageGen** [status] done
- `22:18:43` **Preprocessor** [status] started
- `22:18:54` **Preprocessor** [decision] selected best candidate (score 0.84): G:\codes\mew3d\results\20260826_221801_a-wooden-pirate-ship\intermediate\candidate_02_seed689039460.png
- `22:18:54` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `22:18:54` **Preprocessor** [status] done
- `22:18:54` **MeshGen** [status] started
- `22:19:06` **MeshGen** [artifact] 4 preview renders saved
- `22:19:06` **MeshGen** [artifact] turntable gif saved
- `22:19:08` **MeshGen** [status] done
- `22:19:08` **Judge** [status] started
- `22:19:11` **Judge** [decision] score 0.84 - PASS
- `22:19:11` **Judge** [status] done
- `22:19:11` **Exporter** [status] started
- `22:19:12` **Exporter** [artifact] OBJ exported
- `22:19:12` **Exporter** [artifact] GLB exported (vertex colors included)
