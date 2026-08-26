# Mew3D Run Report - 20260826_211838_first-test

- **Date:** 2026-08-26 21:19:16
- **Mode:** text23d
- **Text input:** a red apple
- **Analyst read:** apple (food, complexity low)

## Prompt enhancement
- Original: `a red apple`
- Enhanced: `A ripe red apple, centered in the frame, displayed in a 3/4 view against a plain white background with even studio lighting, showcasing its glossy surface and natural curves.`
- Negative: `no clutter, no shadows, no text, no watermarks`
- Selected candidate: `G:\codes\mew3d\results\20260826_211838_first-test\intermediate\candidate_00_seed1476763903.png`

## Quality verdict
- **Score:** 1.0 (PASS)
- Attempts: 1
- Faces: 161,788 | Vertices: 81,350 | Watertight: True | Components: 279
- Attempt 1 LLM opinion: The mesh quality is high with a good heuristic score, but the presence of degenerate faces and multiple components is a concern.

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `21:18:40` **Analyst** [status] started
- `21:18:43` **Analyst** [decision] subject 'apple' (food, complexity low) - This is a straightforward request for a single object, proceed with generating the apple.
- `21:18:43` **Analyst** [decision] pipeline plan: PromptSmith -> ImageGen -> Preprocessor -> MeshGen -> Judge -> Exporter
- `21:18:43` **Analyst** [status] done
- `21:18:43` **PromptSmith** [status] started
- `21:18:46` **PromptSmith** [decision] LLM-enhanced prompt: 'A ripe red apple, centered in the frame, displayed in a 3/4 view against a plain white background with even studio lighting, showcasing its glossy surface and natural curves.'
- `21:18:46` **PromptSmith** [status] done
- `21:18:46` **ImageGen** [status] started
- `21:18:57` **ImageGen** [artifact] candidate 1 saved
- `21:18:57` **ImageGen** [artifact] candidate 2 saved
- `21:18:57` **ImageGen** [status] done
- `21:18:57` **Preprocessor** [status] started
- `21:18:59` **Preprocessor** [decision] selected best candidate (score 0.78): G:\codes\mew3d\results\20260826_211838_first-test\intermediate\candidate_00_seed1476763903.png
- `21:18:59` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `21:18:59` **Preprocessor** [status] done
- `21:18:59` **MeshGen** [status] started
- `21:19:10` **MeshGen** [artifact] 4 preview renders saved
- `21:19:10` **MeshGen** [artifact] turntable gif saved
- `21:19:12` **MeshGen** [status] done
- `21:19:12` **Judge** [status] started
- `21:19:15` **Judge** [decision] score 1.00 - PASS
- `21:19:15` **Judge** [status] done
- `21:19:15` **Exporter** [status] started
- `21:19:16` **Exporter** [artifact] OBJ exported
- `21:19:16` **Exporter** [artifact] GLB exported (vertex colors included)
