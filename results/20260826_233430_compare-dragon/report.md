# Mew3D Run Report - 20260826_233430_compare-dragon

- **Date:** 2026-08-26 23:35:50
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\results\20260826_212307_dragon\intermediate\candidate_02_seed272048446.png
- **Analyst read:** dragon (creature, complexity high)
- Selected candidate: `G:\codes\mew3d\results\20260826_233430_compare-dragon\input\user_image.png`

## Backend comparison

| backend | score | faces | components | vision issue |
|---|---|---|---|---|
| triposr **(winner)** | 0.85 | 169,342 | 53 | proportions could be improved |
| hunyuan | 0.332 | 823,956 | 13 | The shape does not resemble a dragon; it appears more like a creature with elephant-like features. |

## Quality verdict
- **Score:** 0.85 (PASS)
- Attempts: 1
- Faces: 169,342 | Vertices: 84,689 | Watertight: False | Components: 53
- Attempt 1 LLM opinion: The mesh quality is high but lacks watertightness and has multiple components.

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `23:34:30` **Analyst** [status] started
- `23:34:34` **Analyst** [decision] subject 'dragon' (creature, complexity high) - Ensure to capture the intricate details of the scales and facial features for a realistic reconstruction.
- `23:34:34` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `23:34:34` **Analyst** [status] done
- `23:34:34` **Preprocessor** [status] started
- `23:34:35` **Preprocessor** [artifact] user image copied to run folder
- `23:34:37` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `23:34:37` **Preprocessor** [status] done
- `23:34:37` **MeshGen** [status] started
- `23:34:50` **MeshGen** [artifact] triposr turntable gif saved
- `23:35:41` **MeshGen** [artifact] hunyuan clay previews saved
- `23:35:41` **MeshGen** [status] done
- `23:35:41` **Judge** [status] started
- `23:35:48` **Judge** [decision] backend comparison: triposr 0.85 | hunyuan 0.33 -> winner: triposr
- `23:35:48` **Judge** [decision] score 0.85 - PASS
- `23:35:48` **Judge** [status] done
- `23:35:48` **Exporter** [status] started
- `23:35:49` **Exporter** [artifact] [triposr] OBJ + GLB exported <- WINNER
- `23:35:50` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
