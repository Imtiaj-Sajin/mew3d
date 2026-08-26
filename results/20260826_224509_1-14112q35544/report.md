# Mew3D Run Report - 20260826_224509_1-14112q35544

- **Date:** 2026-08-26 22:45:39
- **Mode:** image23d
- **Image input:** D:\Downloads\1-14112Q35544.jpg
- **Analyst read:** minion (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260826_224509_1-14112q35544\input\user_image.png`

## Quality verdict
- **Score:** 0.92 (PASS)
- Attempts: 1
- Faces: 61,376 | Vertices: 30,690 | Watertight: True | Components: 1
- Attempt 1 LLM opinion: The mesh quality is high with a solid structure, but the presence of degenerate faces is a minor concern.

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `22:45:10` **Analyst** [status] started
- `22:45:12` **Analyst** [decision] subject 'minion' (character, complexity medium) - Ensure to capture the character's distinctive features and avoid cutting off any limbs.
- `22:45:12` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `22:45:12` **Analyst** [status] done
- `22:45:12` **Preprocessor** [status] started
- `22:45:14` **Preprocessor** [artifact] user image copied to run folder
- `22:45:17` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `22:45:17` **Preprocessor** [status] done
- `22:45:17` **MeshGen** [status] started
- `22:45:33` **MeshGen** [artifact] 4 preview renders saved
- `22:45:33` **MeshGen** [artifact] turntable gif saved
- `22:45:36` **MeshGen** [status] done
- `22:45:36` **Judge** [status] started
- `22:45:39` **Judge** [decision] score 0.92 - PASS
- `22:45:39` **Judge** [status] done
- `22:45:39` **Exporter** [status] started
- `22:45:39` **Exporter** [artifact] OBJ exported
- `22:45:39` **Exporter** [artifact] GLB exported (vertex colors included)
