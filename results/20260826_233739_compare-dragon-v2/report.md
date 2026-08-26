# Mew3D Run Report - 20260826_233739_compare-dragon-v2

- **Date:** 2026-08-26 23:39:00
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\results\20260826_212307_dragon\intermediate\candidate_02_seed272048446.png
- **Analyst read:** dragon (creature, complexity high)
- Selected candidate: `G:\codes\mew3d\results\20260826_233739_compare-dragon-v2\input\user_image.png`

## Backend comparison

| backend | score | faces | components | vision issue |
|---|---|---|---|---|
| triposr **(winner)** | 0.89 | 169,342 | 53 | Minor inconsistencies in the head shape and wing positioning |
| hunyuan | 0.85 | 823,956 | 13 | The head shape is slightly off compared to the source. |

## Quality verdict
- **Score:** 0.89 (PASS)
- Attempts: 1
- Faces: 169,342 | Vertices: 84,689 | Watertight: False | Components: 53
- Attempt 1 LLM opinion: The mesh quality is high, but it lacks watertightness and contains multiple components.

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `23:37:40` **Analyst** [status] started
- `23:37:43` **Analyst** [decision] subject 'dragon' (creature, complexity high) - Ensure to capture the intricate details of the scales and facial features for a realistic reconstruction.
- `23:37:43` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `23:37:43` **Analyst** [status] done
- `23:37:43` **Preprocessor** [status] started
- `23:37:45` **Preprocessor** [artifact] user image copied to run folder
- `23:37:47` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `23:37:47` **Preprocessor** [status] done
- `23:37:47` **MeshGen** [status] started
- `23:38:03` **MeshGen** [artifact] triposr turntable gif saved
- `23:38:49` **MeshGen** [artifact] hunyuan clay previews saved
- `23:38:49` **MeshGen** [status] done
- `23:38:49` **Judge** [status] started
- `23:38:59` **Judge** [decision] backend comparison: triposr 0.89 | hunyuan 0.85 -> winner: triposr
- `23:38:59` **Judge** [decision] score 0.89 - PASS
- `23:38:59` **Judge** [status] done
- `23:38:59` **Exporter** [status] started
- `23:38:59` **Exporter** [artifact] [triposr] OBJ + GLB exported <- WINNER
- `23:39:00` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
