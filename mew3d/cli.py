"""Mew3D command line interface.

Usage:
  python -m mew3d generate --text "a cute dragon"
  python -m mew3d generate --image path\\to\\photo.jpg
  python -m mew3d generate --image photo.jpg --text "a wooden chair"
  python -m mew3d doctor
"""

import argparse
import sys

from .config import GenerationConfig, setup_environment


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mew3d", description="Local agentic text/image -> 3D")
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="generate a 3D model")
    gen.add_argument("--text", help="text prompt describing the object")
    gen.add_argument("--image", help="path to an input image")
    gen.add_argument("--name", dest="run_name", help="name for the results folder")
    gen.add_argument("--image-model", choices=["sd-turbo", "sdxl-turbo"], default="sd-turbo")
    gen.add_argument("--candidates", type=int, default=3, help="candidate images to generate")
    gen.add_argument("--steps", type=int, default=4, help="diffusion steps (turbo: 1-4)")
    gen.add_argument("--mesh-model", choices=["triposr", "hunyuan", "both"],
                     default="triposr",
                     help="3D backend; 'both' runs the two models side by side to compare")
    gen.add_argument("--mc-res", type=int, default=256, help="marching cubes resolution")
    gen.add_argument("--foreground-ratio", type=float, default=0.85)
    gen.add_argument("--previews", type=int, default=4, help="preview views to render (0=off)")
    gen.add_argument("--retries", type=int, default=1, help="max retry attempts if judge fails")
    gen.add_argument("--seed", type=int, help="base seed for image generation")
    gen.add_argument("--no-llm", action="store_true", help="skip LLM, heuristic agents only")
    gen.add_argument("--plain", action="store_true", help="plain log output (no live UI)")

    sub.add_parser("doctor", help="check environment: GPU, models, LLM connectivity")
    return parser


def cmd_generate(args) -> int:
    if not args.text and not args.image:
        print("error: provide --text and/or --image", file=sys.stderr)
        return 2
    if args.image:
        from pathlib import Path

        if not Path(args.image).is_file():
            print(f"error: image not found: {args.image}", file=sys.stderr)
            return 2

    cfg = GenerationConfig(
        text=args.text,
        image=args.image,
        run_name=args.run_name,
        image_model=args.image_model,
        num_candidates=args.candidates,
        image_steps=args.steps,
        mesh_model=args.mesh_model,
        mc_resolution=args.mc_res,
        foreground_ratio=args.foreground_ratio,
        n_preview_views=args.previews,
        max_retries=args.retries,
        seed=args.seed,
        use_llm=not args.no_llm,
        plain_ui=args.plain,
    )

    from .core.orchestrator import Orchestrator
    from .core.run_context import RunContext
    from .ui.live import LiveUI

    ctx = RunContext(cfg)
    ui = LiveUI(ctx, plain=cfg.plain_ui)
    try:
        with ui:
            result = Orchestrator(ctx).run()
    except KeyboardInterrupt:
        print("\ninterrupted - partial results in", ctx.dir)
        return 130
    except Exception as e:
        print(f"\nrun failed: {type(e).__name__}: {e}", file=sys.stderr)
        print("logs:", ctx.path("logs", "run.log"), file=sys.stderr)
        raise
    finally:
        ctx.close()

    verdict = result["verdict"]
    print(f"\n=== Mew3D run {ctx.run_id} complete ===")
    print(f"  quality score : {verdict['score']:.2f} "
          f"({'PASS' if verdict['passed'] else 'best effort'})")
    print(f"  mesh          : {result['outputs']['glb']}")
    print(f"  report        : {result['outputs']['report']}")
    return 0


def cmd_doctor() -> int:
    print("Mew3D doctor\n" + "=" * 40)
    ok = True

    try:
        import torch

        cuda = torch.cuda.is_available()
        print(f"[{'OK' if cuda else '!!'}] torch {torch.__version__}, CUDA available: {cuda}")
        if cuda:
            props = torch.cuda.get_device_properties(0)
            print(f"     GPU: {props.name}, {props.total_memory / 1e9:.1f} GB")
        else:
            ok = False
    except ImportError as e:
        print(f"[!!] torch not installed: {e}")
        ok = False

    for mod in ("diffusers", "transformers", "rembg", "trimesh", "skimage", "rich", "einops", "omegaconf"):
        try:
            __import__(mod)
            print(f"[OK] {mod}")
        except ImportError:
            print(f"[!!] {mod} missing")
            ok = False

    from .config import TRIPOSR_DIR

    if (TRIPOSR_DIR / "tsr" / "system.py").is_file():
        print("[OK] TripoSR vendored")
    else:
        print(f"[!!] TripoSR missing at {TRIPOSR_DIR}")
        ok = False

    import os

    key = os.getenv("OPENAI_API_KEY", "")
    if key:
        print(f"[OK] OPENAI_API_KEY set ({key[:6]}...) - agents will try the LLM, "
              "with heuristic fallback")
    else:
        print("[--] OPENAI_API_KEY not set - agents run in heuristic mode")

    print("=" * 40)
    print("environment looks good" if ok else "issues found - see above")
    return 0 if ok else 1


def main(argv=None) -> int:
    # Windows: redirected stdout defaults to the ANSI codepage, which can't encode
    # the agent icons; force UTF-8 so background/piped runs never crash on a print
    for stream in (sys.stdout, sys.stderr):
        if stream and hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    setup_environment()
    args = build_parser().parse_args(argv)
    if args.command == "generate":
        return cmd_generate(args)
    if args.command == "doctor":
        return cmd_doctor()
    return 2
