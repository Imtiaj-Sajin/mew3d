# Mew3D Run Report - 20260827_105356_upload-1787806436

- **Date:** 2026-08-27 10:56:34
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787806436.jpg
- **Analyst read:** donut (food, complexity low)
- Selected candidate: `G:\codes\mew3d\results\20260827_105356_upload-1787806436\input\user_image.png`

## Quality verdict
- **Score:** 0.88 (PASS)
- Attempts: 1
- Faces: 1,055,828 | Vertices: 527,914 | Watertight: True | Components: 1
- Attempt 1 LLM opinion: The mesh quality is generally acceptable but has a concerning number of degenerate faces.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `10:53:56` **Analyst** [status] started
- `10:53:57` **Analyst** [decision] subject 'donut' (food, complexity low) - Ensure to capture the texture of the frosting and sprinkles for a realistic finish.
- `10:53:57` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `10:53:57` **Analyst** [status] done
- `10:53:57` **Preprocessor** [status] started
- `10:53:58` **Preprocessor** [artifact] user image copied to run folder
- `10:54:00` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `10:54:00` **Preprocessor** [status] done
- `10:54:00` **MeshGen** [status] started
- `10:54:51` **MeshGen** [artifact] hunyuan clay previews saved
- `10:54:51` **MeshGen** [status] done
- `10:54:51` **Judge** [status] started
- `10:54:55` **Judge** [decision] score 0.88 - PASS
- `10:54:55` **Judge** [status] done
- `10:54:55` **TextureSmith** [status] started
- `10:56:32` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `10:56:32` **TextureSmith** [artifact] textured previews saved
- `10:56:32` **TextureSmith** [status] done
- `10:56:32` **Exporter** [status] started
- `10:56:34` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
