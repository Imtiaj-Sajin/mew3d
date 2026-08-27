# Mew3D Run Report - 20260827_074243_dragon-textured

- **Date:** 2026-08-27 07:45:44
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\results\20260826_212307_dragon\intermediate\candidate_02_seed272048446.png
- **Analyst read:** dragon (creature, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_074243_dragon-textured\input\user_image.png`

## Quality verdict
- **Score:** 0.89 (PASS)
- Attempts: 1
- Faces: 823,956 | Vertices: 411,976 | Watertight: False | Components: 13
- Attempt 1 LLM opinion: The mesh of the dragon is generally well-constructed but has some issues with watertightness and degeneracy.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `07:42:44` **Analyst** [status] started
- `07:42:47` **Analyst** [decision] subject 'dragon' (creature, complexity medium) - Ensure to capture the intricate details of the scales and facial features for a realistic reconstruction.
- `07:42:47` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `07:42:47` **Analyst** [status] done
- `07:42:47` **Preprocessor** [status] started
- `07:42:49` **Preprocessor** [artifact] user image copied to run folder
- `07:42:51` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `07:42:51` **Preprocessor** [status] done
- `07:42:51` **MeshGen** [status] started
- `07:43:47` **MeshGen** [artifact] hunyuan clay previews saved
- `07:43:47` **MeshGen** [status] done
- `07:43:47` **Judge** [status] started
- `07:43:52` **Judge** [decision] score 0.89 - PASS
- `07:43:52` **Judge** [status] done
- `07:43:52` **TextureSmith** [status] started
- `07:45:43` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `07:45:43` **TextureSmith** [status] done
- `07:45:43` **Exporter** [status] started
- `07:45:44` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
