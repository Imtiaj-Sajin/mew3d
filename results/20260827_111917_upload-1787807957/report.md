# Mew3D Run Report - 20260827_111917_upload-1787807957

- **Date:** 2026-08-27 11:21:53
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787807957.jpg
- **Analyst read:** headphones (prop, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_111917_upload-1787807957\input\user_image.png`

## Quality verdict
- **Score:** 0.85 (PASS)
- Attempts: 1
- Faces: 850,628 | Vertices: 425,311 | Watertight: False | Components: 2
- Attempt 1 LLM opinion: The mesh quality is high but concerns about watertightness and degenerate faces need to be addressed.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `11:19:17` **Analyst** [status] started
- `11:19:18` **Analyst** [decision] subject 'headphones' (prop, complexity medium) - Ensure to capture the details of the ear cups and headband for accurate reconstruction.
- `11:19:18` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `11:19:18` **Analyst** [status] done
- `11:19:18` **Preprocessor** [status] started
- `11:19:19` **Preprocessor** [artifact] user image copied to run folder
- `11:19:21` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `11:19:21` **Preprocessor** [status] done
- `11:19:21` **MeshGen** [status] started
- `11:20:09` **MeshGen** [artifact] hunyuan clay previews saved
- `11:20:09` **MeshGen** [status] done
- `11:20:09` **Judge** [status] started
- `11:20:13` **Judge** [decision] score 0.85 - PASS
- `11:20:13` **Judge** [status] done
- `11:20:13` **TextureSmith** [status] started
- `11:21:51` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `11:21:52` **TextureSmith** [artifact] textured previews saved
- `11:21:52` **TextureSmith** [status] done
- `11:21:52` **Exporter** [status] started
- `11:21:53` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
