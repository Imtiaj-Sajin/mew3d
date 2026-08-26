# Mew3D Run Report - 20260826_230014_sntp7ftarj22lsvekn47eepqrxyn033p

- **Date:** 2026-08-26 23:00:45
- **Mode:** image23d
- **Image input:** D:\Downloads\sntp7ftaRJ22lsVEkn47eePQRXYn033Pyg2W7lkA.jpeg
- **Analyst read:** house (architecture, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260826_230014_sntp7ftarj22lsvekn47eepqrxyn033p\input\user_image.png`

## Quality verdict
- **Score:** 0.88 (PASS)
- Attempts: 1
- Faces: 116,496 | Vertices: 58,270 | Watertight: True | Components: 12
- Attempt 1 LLM opinion: The mesh quality is high with a watertight structure, but the presence of multiple components and a few degenerate faces may need attention.

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `23:00:15` **Analyst** [status] started
- `23:00:20` **Analyst** [decision] subject 'house' (architecture, complexity medium) - Ensure to capture the details of the roof and windows for accurate reconstruction.
- `23:00:20` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `23:00:20` **Analyst** [status] done
- `23:00:20` **Preprocessor** [status] started
- `23:00:22` **Preprocessor** [artifact] user image copied to run folder
- `23:00:24` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `23:00:24` **Preprocessor** [status] done
- `23:00:24` **MeshGen** [status] started
- `23:00:40` **MeshGen** [artifact] triposr turntable gif saved
- `23:00:42` **MeshGen** [status] done
- `23:00:42` **Judge** [status] started
- `23:00:45` **Judge** [decision] score 0.88 - PASS
- `23:00:45` **Judge** [status] done
- `23:00:45` **Exporter** [status] started
- `23:00:45` **Exporter** [artifact] [triposr] OBJ + GLB exported
