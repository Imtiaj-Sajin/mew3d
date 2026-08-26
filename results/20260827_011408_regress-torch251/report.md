# Mew3D Run Report - 20260827_011408_regress-torch251

- **Date:** 2026-08-27 01:15:36
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\results\20260826_212307_dragon\intermediate\candidate_02_seed272048446.png
- **Analyst read:** dragon (creature, complexity high)
- Selected candidate: `G:\codes\mew3d\results\20260827_011408_regress-torch251\input\user_image.png`

## Quality verdict
- **Score:** 0.89 (PASS)
- Attempts: 1
- Faces: 823,956 | Vertices: 411,976 | Watertight: False | Components: 13
- Attempt 1 LLM opinion: The mesh displays high quality but is not watertight, which is a significant issue for certain applications.

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `01:14:09` **Analyst** [status] started
- `01:14:12` **Analyst** [decision] subject 'dragon' (creature, complexity high) - Ensure to capture the intricate details of the scales and the unique features of the wings.
- `01:14:12` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `01:14:12` **Analyst** [status] done
- `01:14:12` **Preprocessor** [status] started
- `01:14:15` **Preprocessor** [artifact] user image copied to run folder
- `01:14:18` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `01:14:18` **Preprocessor** [status] done
- `01:14:18` **MeshGen** [status] started
- `01:15:30` **MeshGen** [artifact] hunyuan clay previews saved
- `01:15:30` **MeshGen** [status] done
- `01:15:30` **Judge** [status] started
- `01:15:35` **Judge** [decision] score 0.89 - PASS
- `01:15:35` **Judge** [status] done
- `01:15:35` **Exporter** [status] started
- `01:15:36` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
