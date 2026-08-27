# Mew3D Run Report - 20260827_181918_upload-1787833158

- **Date:** 2026-08-27 18:22:10
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787833158.jpg
- **Analyst read:** motorcycle (vehicle, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_181918_upload-1787833158\input\user_image.png`

## Quality verdict
- **Score:** 0.92 (PASS)
- Attempts: 1
- Faces: 467,788 | Vertices: 233,874 | Watertight: True | Components: 4
- Attempt 1 LLM opinion: The mesh is generally well-constructed but exhibits some concerns regarding component integrity and degenerate faces.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `18:19:18` **Analyst** [status] started
- `18:19:20` **Analyst** [decision] subject 'motorcycle' (vehicle, complexity medium) - Ensure to capture the unique design features and contours of the motorcycle for accurate reconstruction.
- `18:19:20` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `18:19:20` **Analyst** [status] done
- `18:19:20` **Preprocessor** [status] started
- `18:19:22` **Preprocessor** [artifact] user image copied to run folder
- `18:19:24` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `18:19:24` **Preprocessor** [status] done
- `18:19:24` **Gatekeeper** [status] started
- `18:19:25` **Gatekeeper** [decision] prepared image looks reconstructable - handing to MeshGen
- `18:19:25` **Gatekeeper** [status] done
- `18:19:25` **MeshGen** [status] started
- `18:20:09` **MeshGen** [artifact] hunyuan clay previews saved
- `18:20:09` **MeshGen** [status] done
- `18:20:09` **Judge** [status] started
- `18:20:12` **Judge** [decision] score 0.92 - PASS
- `18:20:12` **Judge** [status] done
- `18:20:12` **TextureSmith** [status] started
- `18:22:09` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `18:22:09` **TextureSmith** [artifact] textured previews saved
- `18:22:09` **TextureSmith** [status] done
- `18:22:09` **Exporter** [status] started
- `18:22:10` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
