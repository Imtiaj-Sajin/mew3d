# Mew3D Run Report - 20260826_212624_image-mode-good

- **Date:** 2026-08-26 21:26:51
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\results\20260826_212307_dragon\intermediate\candidate_02_seed272048446.png
- **Analyst read:** dragon (creature, complexity high)
- Selected candidate: `G:\codes\mew3d\results\20260826_212624_image-mode-good\input\user_image.png`

## Quality verdict
- **Score:** 0.89 (PASS)
- Attempts: 1
- Faces: 169,342 | Vertices: 84,689 | Watertight: False | Components: 53
- Attempt 1 LLM opinion: The mesh quality is high, but it is not watertight and contains some degenerate faces.

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `21:26:25` **Analyst** [status] started
- `21:26:27` **Analyst** [decision] subject 'dragon' (creature, complexity high) - Ensure to capture the intricate details of the scales and facial features for a more realistic reconstruction.
- `21:26:27` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `21:26:27` **Analyst** [status] done
- `21:26:27` **Preprocessor** [status] started
- `21:26:29` **Preprocessor** [artifact] user image copied to run folder
- `21:26:32` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `21:26:32` **Preprocessor** [status] done
- `21:26:32` **MeshGen** [status] started
- `21:26:45` **MeshGen** [artifact] 4 preview renders saved
- `21:26:45` **MeshGen** [artifact] turntable gif saved
- `21:26:47` **MeshGen** [status] done
- `21:26:47` **Judge** [status] started
- `21:26:51` **Judge** [decision] score 0.89 - PASS
- `21:26:51` **Judge** [status] done
- `21:26:51` **Exporter** [status] started
- `21:26:51` **Exporter** [artifact] OBJ exported
- `21:26:51` **Exporter** [artifact] GLB exported (vertex colors included)
