# Mew3D Run Report - 20260827_002558_cute-mashro

- **Date:** 2026-08-27 00:27:24
- **Mode:** image23d
- **Image input:** D:\Downloads\cute mashro.jpg
- **Analyst read:** mushroom (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_002558_cute-mashro\input\user_image.png`

## Backend comparison

| backend | score | faces | components | vision issue |
|---|---|---|---|---|
| triposr | 0.89 | 176,724 | 7 | Slight inconsistencies in the shape of the cap |
| hunyuan **(winner)** | 0.93 | 1,176,936 | 5 | none |

## Quality verdict
- **Score:** 0.93 (PASS)
- Attempts: 1
- Faces: 1,176,936 | Vertices: 588,468 | Watertight: False | Components: 5
- Attempt 1 LLM opinion: The mesh quality is high but requires improvement in watertightness and reduction of degenerate faces.

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `00:25:59` **Analyst** [status] started
- `00:26:01` **Analyst** [decision] subject 'mushroom' (character, complexity medium) - Ensure to capture the rounded shapes and facial features for a cute appearance.
- `00:26:01` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `00:26:01` **Analyst** [status] done
- `00:26:01` **Preprocessor** [status] started
- `00:26:03` **Preprocessor** [artifact] user image copied to run folder
- `00:26:04` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `00:26:04` **Preprocessor** [status] done
- `00:26:04` **MeshGen** [status] started
- `00:26:21` **MeshGen** [artifact] triposr turntable gif saved
- `00:27:14` **MeshGen** [artifact] hunyuan clay previews saved
- `00:27:14` **MeshGen** [status] done
- `00:27:14` **Judge** [status] started
- `00:27:22` **Judge** [decision] backend comparison: hunyuan 0.93 | triposr 0.89 -> winner: hunyuan
- `00:27:22` **Judge** [decision] score 0.93 - PASS
- `00:27:22` **Judge** [status] done
- `00:27:22` **Exporter** [status] started
- `00:27:22` **Exporter** [artifact] [triposr] OBJ + GLB exported
- `00:27:24` **Exporter** [artifact] [hunyuan] OBJ + GLB exported <- WINNER
