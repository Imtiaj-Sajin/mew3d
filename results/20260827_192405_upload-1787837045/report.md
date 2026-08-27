# Mew3D Run Report - 20260827_192405_upload-1787837045

- **Date:** 2026-08-27 19:27:02
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787837045.webp
- **Analyst read:** scooter (vehicle, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_192405_upload-1787837045\input\user_image.png`

## Quality verdict
- **Score:** 0.74 (PASS)
- Attempts: 1
- Faces: 858,946 | Vertices: 429,405 | Watertight: False | Components: 6
- Attempt 1 concern: fragmented: 6 pieces, main piece only 78% of faces
- Attempt 1 LLM opinion: The mesh quality is acceptable but has several significant issues that need addressing.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `19:24:05` **Analyst** [status] started
- `19:24:07` **Analyst** [decision] subject 'scooter' (vehicle, complexity medium) - Ensure to capture the details of the scooter's design and color for accurate reconstruction.
- `19:24:07` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `19:24:07` **Analyst** [status] done
- `19:24:07` **Preprocessor** [status] started
- `19:24:08` **Preprocessor** [artifact] user image copied to run folder
- `19:24:10` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `19:24:10` **Preprocessor** [status] done
- `19:24:10` **Gatekeeper** [status] started
- `19:24:12` **Gatekeeper** [decision] prepared image looks reconstructable - handing to MeshGen
- `19:24:12` **Gatekeeper** [status] done
- `19:24:12` **MeshGen** [status] started
- `19:25:04` **MeshGen** [artifact] hunyuan clay previews saved
- `19:25:04` **MeshGen** [status] done
- `19:25:04` **Judge** [status] started
- `19:25:08` **Judge** [decision] score 0.74 - PASS
- `19:25:08` **Judge** [status] done
- `19:25:08` **TextureSmith** [status] started
- `19:27:00` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `19:27:01` **TextureSmith** [artifact] textured previews saved
- `19:27:01` **TextureSmith** [status] done
- `19:27:01` **Exporter** [status] started
- `19:27:02` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
