# Mew3D Run Report - 20260827_085721_upload-1787799441

- **Date:** 2026-08-27 09:00:06
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787799441.jpg
- **Analyst read:** blue spinner (prop, complexity low)
- Selected candidate: `G:\codes\mew3d\results\20260827_085721_upload-1787799441\input\user_image.png`

## Quality verdict
- **Score:** 0.92 (PASS)
- Attempts: 1
- Faces: 476,580 | Vertices: 238,292 | Watertight: True | Components: 1
- Attempt 1 LLM opinion: The mesh quality is satisfactory with a high heuristic score, but the presence of degenerate faces raises some concerns.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `08:57:21` **Analyst** [status] started
- `08:57:24` **Analyst** [decision] subject 'blue spinner' (prop, complexity low) - Ensure the spinner is well-lit and centered in the frame for accurate reconstruction.
- `08:57:24` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `08:57:24` **Analyst** [status] done
- `08:57:24` **Preprocessor** [status] started
- `08:57:26` **Preprocessor** [artifact] user image copied to run folder
- `08:57:36` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `08:57:36` **Preprocessor** [status] done
- `08:57:36` **MeshGen** [status] started
- `08:58:17` **MeshGen** [artifact] hunyuan clay previews saved
- `08:58:17` **MeshGen** [status] done
- `08:58:17` **Judge** [status] started
- `08:58:21` **Judge** [decision] score 0.92 - PASS
- `08:58:21` **Judge** [status] done
- `08:58:21` **TextureSmith** [status] started
- `09:00:05` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `09:00:06` **TextureSmith** [artifact] textured previews saved
- `09:00:06` **TextureSmith** [status] done
- `09:00:06` **Exporter** [status] started
- `09:00:06` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
