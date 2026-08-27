# Mew3D Run Report - 20260827_102252_upload-1787804572

- **Date:** 2026-08-27 10:25:55
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787804572.jpg
- **Analyst read:** warrior character (character, complexity high)
- Selected candidate: `G:\codes\mew3d\results\20260827_102252_upload-1787804572\input\user_image.png`

## Quality verdict
- **Score:** 0.85 (PASS)
- Attempts: 1
- Faces: 1,145,732 | Vertices: 572,661 | Watertight: False | Components: 26
- Attempt 1 LLM opinion: The mesh is largely detailed but has significant issues with non-watertightness and multiple components.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `10:22:52` **Analyst** [status] started
- `10:22:53` **Analyst** [decision] subject 'warrior character' (character, complexity high) - Ensure to capture the intricate details of the armor and weaponry for a realistic reconstruction.
- `10:22:53` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `10:22:53` **Analyst** [status] done
- `10:22:53` **Preprocessor** [status] started
- `10:22:54` **Preprocessor** [artifact] user image copied to run folder
- `10:22:57` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `10:22:57` **Preprocessor** [status] done
- `10:22:57` **MeshGen** [status] started
- `10:23:50` **MeshGen** [artifact] hunyuan clay previews saved
- `10:23:50` **MeshGen** [status] done
- `10:23:50` **Judge** [status] started
- `10:23:56` **Judge** [decision] score 0.85 - PASS
- `10:23:56` **Judge** [status] done
- `10:23:56` **TextureSmith** [status] started
- `10:25:53` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `10:25:54` **TextureSmith** [artifact] textured previews saved
- `10:25:54` **TextureSmith** [status] done
- `10:25:54` **Exporter** [status] started
- `10:25:55` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
