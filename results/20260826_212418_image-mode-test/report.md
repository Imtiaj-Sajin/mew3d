# Mew3D Run Report - 20260826_212418_image-mode-test

- **Date:** 2026-08-26 21:25:24
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\results\20260826_212151_apple-v2\intermediate\candidate_00_seed1620037284.png
- **Analyst read:** candidate 00 (other, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260826_212418_image-mode-test\input\user_image.png`

## Quality verdict
- **Score:** 0.35 (below threshold, best effort)
- Attempts: 3
- Faces: 395,152 | Vertices: 197,842 | Watertight: True | Components: 237
- Attempt 1 LLM opinion: The mesh is well-structured and meets quality standards, but the presence of degenerate faces is a concern.
- Attempt 2 LLM opinion: The mesh has a high heuristic score but significant issues with watertightness and component fragmentation.
- Attempt 3 LLM opinion: The mesh quality is acceptable with a high heuristic score, but there are concerns regarding the presence of degenerate faces and multiple components.

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `21:24:19` **Analyst** [status] started
- `21:24:21` **Analyst** [decision] subject 'candidate 00' (other, complexity medium) - Focus on identifying and isolating the main subject for a better 3D reconstruction.
- `21:24:21` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `21:24:21` **Analyst** [status] done
- `21:24:21` **Preprocessor** [status] started
- `21:24:23` **Preprocessor** [artifact] user image copied to run folder
- `21:24:25` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `21:24:25` **Preprocessor** [status] done
- `21:24:25` **MeshGen** [status] started
- `21:24:38` **MeshGen** [artifact] 4 preview renders saved
- `21:24:38` **MeshGen** [artifact] turntable gif saved
- `21:24:41` **MeshGen** [status] done
- `21:24:41` **Judge** [status] started
- `21:24:44` **Judge** [decision] score 0.35 < 0.55 - requesting retry with {'foreground_ratio': 0.75, 'mc_resolution': 320}
- `21:24:44` **Judge** [status] done
- `21:24:44` **Preprocessor** [status] started
- `21:24:47` **Preprocessor** [artifact] processed input ready (foreground ratio 0.75)
- `21:24:47` **Preprocessor** [status] done
- `21:24:47` **MeshGen** [status] started
- `21:24:50` **MeshGen** [artifact] 4 preview renders saved
- `21:24:51` **MeshGen** [artifact] turntable gif saved
- `21:24:55` **MeshGen** [status] done
- `21:24:55` **Judge** [status] started
- `21:25:06` **Judge** [decision] score 0.33 < 0.55 - requesting retry with {'foreground_ratio': 0.65, 'mc_resolution': 320}
- `21:25:06` **Judge** [status] done
- `21:25:06` **Preprocessor** [status] started
- `21:25:08` **Preprocessor** [artifact] processed input ready (foreground ratio 0.65)
- `21:25:08` **Preprocessor** [status] done
- `21:25:08` **MeshGen** [status] started
- `21:25:12` **MeshGen** [artifact] 4 preview renders saved
- `21:25:12` **MeshGen** [artifact] turntable gif saved
- `21:25:16` **MeshGen** [status] done
- `21:25:16` **Judge** [status] started
- `21:25:23` **Judge** [decision] score 0.35 - accepting best effort (no retries left)
- `21:25:23` **Judge** [status] done
- `21:25:23` **Exporter** [status] started
- `21:25:24` **Exporter** [artifact] OBJ exported
- `21:25:24` **Exporter** [artifact] GLB exported (vertex colors included)
