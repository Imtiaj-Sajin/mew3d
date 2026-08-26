# Mew3D Run Report - 20260827_002009_face-man

- **Date:** 2026-08-27 00:20:41
- **Mode:** image23d
- **Image input:** D:\Downloads\face man.jpg
- **Analyst read:** male character (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_002009_face-man\input\user_image.png`

## Quality verdict
- **Score:** 0.92 (PASS)
- Attempts: 1
- Faces: 116,428 | Vertices: 58,216 | Watertight: True | Components: 1
- Attempt 1 LLM opinion: The mesh of the male character is well-constructed and meets quality standards.

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `00:20:10` **Analyst** [status] started
- `00:20:13` **Analyst** [decision] subject 'male character' (character, complexity medium) - Ensure to capture the facial features and hair details accurately for a realistic reconstruction.
- `00:20:13` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `00:20:13` **Analyst** [status] done
- `00:20:13` **Preprocessor** [status] started
- `00:20:16` **Preprocessor** [artifact] user image copied to run folder
- `00:20:18` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `00:20:18` **Preprocessor** [status] done
- `00:20:18` **MeshGen** [status] started
- `00:20:35` **MeshGen** [artifact] triposr turntable gif saved
- `00:20:37` **MeshGen** [status] done
- `00:20:37` **Judge** [status] started
- `00:20:40` **Judge** [decision] score 0.92 - PASS
- `00:20:40` **Judge** [status] done
- `00:20:40` **Exporter** [status] started
- `00:20:41` **Exporter** [artifact] [triposr] OBJ + GLB exported
