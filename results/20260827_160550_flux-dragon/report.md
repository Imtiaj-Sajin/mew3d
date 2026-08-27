# Mew3D Run Report - 20260827_160550_flux-dragon

- **Date:** 2026-08-27 16:09:18
- **Mode:** text23d
- **Text input:** a cute baby dragon
- **Analyst read:** baby dragon (creature, complexity medium)

## Prompt enhancement
- Original: `a cute baby dragon`
- Enhanced: `full view of a whole cute baby dragon with large sparkling eyes and small wings, centered against a plain light background`
- Negative: `close-up, macro, cropped`
- Selected candidate: `G:\codes\mew3d\results\20260827_160550_flux-dragon\intermediate\candidate_02_seed1744394220.png`

## Quality verdict
- **Score:** 0.93 (PASS)
- Attempts: 1
- Faces: 897,608 | Vertices: 448,799 | Watertight: False | Components: 15
- Attempt 1 LLM opinion: The mesh quality is high, but the lack of watertightness and presence of degenerate faces are concerning.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `16:05:51` **Guardian** [status] started
- `16:05:52` **Guardian** [status] done
- `16:05:52` **Analyst** [status] started
- `16:05:53` **Analyst** [decision] subject 'baby dragon' (creature, complexity medium) - Ensure the design emphasizes the cute features of the dragon for better appeal.
- `16:05:53` **Analyst** [decision] pipeline plan: PromptSmith -> ImageGen -> Preprocessor -> MeshGen -> Judge -> Exporter
- `16:05:53` **Analyst** [status] done
- `16:05:53` **PromptSmith** [status] started
- `16:05:56` **PromptSmith** [decision] LLM-enhanced prompt: 'full view of a whole cute baby dragon with large sparkling eyes and small wings, centered against a plain light background'
- `16:05:56` **PromptSmith** [status] done
- `16:05:56` **ImageGen** [status] started
- `16:06:02` **ImageGen** [artifact] candidate 1 saved
- `16:06:07` **ImageGen** [artifact] candidate 2 saved
- `16:06:11` **ImageGen** [artifact] candidate 3 saved
- `16:06:11` **ImageGen** [status] done
- `16:06:11` **Preprocessor** [status] started
- `16:06:20` **Preprocessor** [decision] selected best candidate (score 0.96): G:\codes\mew3d\results\20260827_160550_flux-dragon\intermediate\candidate_02_seed1744394220.png
- `16:06:20` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `16:06:20` **Preprocessor** [status] done
- `16:06:20` **Gatekeeper** [status] started
- `16:06:22` **Gatekeeper** [decision] prepared image looks reconstructable - handing to MeshGen
- `16:06:22` **Gatekeeper** [status] done
- `16:06:22` **MeshGen** [status] started
- `16:07:29` **MeshGen** [artifact] hunyuan clay previews saved
- `16:07:29` **MeshGen** [status] done
- `16:07:29` **Judge** [status] started
- `16:07:33` **Judge** [decision] score 0.93 - PASS
- `16:07:33` **Judge** [status] done
- `16:07:33` **TextureSmith** [status] started
- `16:09:16` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `16:09:17` **TextureSmith** [artifact] textured previews saved
- `16:09:17` **TextureSmith** [status] done
- `16:09:17` **Exporter** [status] started
- `16:09:18` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
