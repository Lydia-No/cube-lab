from __future__ import annotations

import argparse
import importlib
import sys
from typing import Callable

from edge_memory import EdgeMode


def _load_callable(module_name: str, func_name: str = "run") -> Callable[[], None]:
    mod = importlib.import_module(module_name)
    fn = getattr(mod, func_name, None)
    if fn is None or not callable(fn):
        raise SystemExit(f"{module_name}.{func_name} not found or not callable")
    return fn


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="cube_cli.py", description="Hypercube Observer CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("cube", help="Basic cube walk demo")
    sub.add_parser("network", help="Cube network growth demo")
    sub.add_parser("sky", help="Observer sky demo")
    sub.add_parser("tesseract", help="Tesseract demo (if present)")

    interior = sub.add_parser("interior", help="Interior field + observer view + hybrid edge memory")
    interior.add_argument("--dim", type=int, default=3)
    interior.add_argument("--steps", type=int, default=600)
    interior.add_argument("--seed", type=int, default=1)
    interior.add_argument("--activation-decay", type=float, default=0.995)
    interior.add_argument("--activation-pulse", type=float, default=1.0)
    interior.add_argument("--edge-mode", type=str, default="hybrid", choices=["persist", "decay", "hybrid"])
    interior.add_argument("--edge-decay", type=float, default=0.995)
    interior.add_argument("--fast-decay", type=float, default=0.990)
    interior.add_argument("--slow-decay", type=float, default=0.9995)
    interior.add_argument("--consolidate-threshold", type=float, default=8.0)
    interior.add_argument("--consolidate-amount", type=float, default=4.0)
    interior.add_argument("--fast-min-weight", type=float, default=2.0)
    interior.add_argument("--slow-min-weight", type=float, default=3.0)
    interior.add_argument("--observer-view", action="store_true")
    interior.add_argument("--edge-view", type=str, default="sky", choices=["sky", "chord"])
    interior.add_argument("--region-depth", type=float, default=0.75)
    interior.add_argument("--jitter", type=float, default=0.05)
    interior.add_argument("--pulse-boost", type=float, default=14.0)
    interior.add_argument("--pulse-tau", type=float, default=35.0)
    interior.add_argument("--save-html", type=str, default=None)
    interior.add_argument("--save-png", type=str, default=None)
    interior.add_argument("--png-width", type=int, default=1400)
    interior.add_argument("--png-height", type=int, default=900)
    interior.add_argument("--png-scale", type=float, default=2.0)

    metrics = sub.add_parser("metrics", help="Windowed metrics (requires metrics_demo.py)")
    metrics.add_argument("--dim", type=int, default=3)
    metrics.add_argument("--steps", type=int, default=5000)
    metrics.add_argument("--window", type=int, default=200)

    # Forwarders with real help
    signature = sub.add_parser("signature", help="Forward to signature_demo.py signature ...")
    signature.add_argument("--dim", type=int, default=3)
    signature.add_argument("--steps", type=int, default=2000)
    signature.add_argument("--seed", type=int, default=1)
    signature.add_argument("--slow-min-weight", type=float, default=3.0)
    signature.add_argument("--top-edges", type=int, default=20)

    cluster = sub.add_parser("cluster", help="Forward to signature_demo.py cluster ...")
    cluster.add_argument("--n", type=int, default=50)
    cluster.add_argument("--dim", type=int, default=3)
    cluster.add_argument("--steps", type=int, default=2000)
    cluster.add_argument("--seed0", type=int, default=1)
    cluster.add_argument("--slow-min-weight", type=float, default=3.0)
    cluster.add_argument("--top-edges", type=int, default=20)

    synth = sub.add_parser("synth", help="Forward to synth_demo.py (search + optional render)")
    synth.add_argument("--dim", type=int, default=3)
    synth.add_argument("--steps", type=int, default=700)
    synth.add_argument("--motif", type=str, default="square", choices=["square", "hub", "bridge", "two_cycle"])
    synth.add_argument("--iters", type=int, default=500)
    synth.add_argument("--restarts", type=int, default=12)
    synth.add_argument("--slow-min-weight", type=float, default=3.0)
    synth.add_argument("--seed", type=int, default=1)
    synth.add_argument("--out-actions", type=str, default="best_actions.json")
    synth.add_argument("--render-html", type=str, default=None)
    synth.add_argument("--render-png", type=str, default=None)
    synth.add_argument("--observer-view", action="store_true")
    synth.add_argument("--edge-view", type=str, default="sky", choices=["sky", "chord"])

    args = parser.parse_args(argv)

    if args.cmd == "cube":
        _load_callable("cube_demo", "run")()
        return 0
    if args.cmd == "network":
        _load_callable("cube_network_demo", "run")()
        return 0
    if args.cmd == "sky":
        _load_callable("observer_sky_demo", "run")()
        return 0
    if args.cmd == "tesseract":
        try:
            _load_callable("tesseract_demo", "run")()
        except SystemExit:
            _load_callable("tesseract_demo", "main")()
        return 0

    if args.cmd == "interior":
        import interior_field_demo as demo
        demo.run(
            dim=args.dim,
            steps=args.steps,
            activation_decay=args.activation_decay,
            activation_pulse=args.activation_pulse,
            edge_mode=EdgeMode(args.edge_mode),
            edge_decay=args.edge_decay,
            fast_decay=args.fast_decay,
            slow_decay=args.slow_decay,
            consolidate_threshold=args.consolidate_threshold,
            consolidate_amount=args.consolidate_amount,
            fast_min_weight=args.fast_min_weight,
            slow_min_weight=args.slow_min_weight,
            observer_view=args.observer_view,
            edge_view=args.edge_view,
            region_depth=args.region_depth,
            jitter=args.jitter,
            seed=args.seed,
            pulse_boost=args.pulse_boost,
            pulse_tau=args.pulse_tau,
            save_html=args.save_html,
            save_png=args.save_png,
            png_width=args.png_width,
            png_height=args.png_height,
            png_scale=args.png_scale,
        )
        return 0

    if args.cmd == "metrics":
        mod = importlib.import_module("metrics_demo")
        main_fn = getattr(mod, "main", None)
        if not callable(main_fn):
            raise SystemExit("metrics_demo.main not found")
        sys.argv = ["metrics_demo.py"]
        main_fn()
        return 0

    if args.cmd == "signature":
        import signature_demo as s
        sys.argv = [
            "signature_demo.py",
            "signature",
            "--dim", str(args.dim),
            "--steps", str(args.steps),
            "--seed", str(args.seed),
            "--slow-min-weight", str(args.slow_min_weight),
            "--top-edges", str(args.top_edges),
        ]
        s.main()
        return 0

    if args.cmd == "cluster":
        import signature_demo as s
        sys.argv = [
            "signature_demo.py",
            "cluster",
            "--n", str(args.n),
            "--dim", str(args.dim),
            "--steps", str(args.steps),
            "--seed0", str(args.seed0),
            "--slow-min-weight", str(args.slow_min_weight),
            "--top-edges", str(args.top_edges),
        ]
        s.main()
        return 0

    if args.cmd == "synth":
        import synth_demo as sd
        sys.argv = [
            "synth_demo.py",
            "--dim", str(args.dim),
            "--steps", str(args.steps),
            "--motif", str(args.motif),
            "--iters", str(args.iters),
            "--restarts", str(args.restarts),
            "--slow-min-weight", str(args.slow_min_weight),
            "--seed", str(args.seed),
            "--out-actions", str(args.out_actions),
        ]
        if args.render_html:
            sys.argv += ["--render-html", args.render_html]
        if args.render_png:
            sys.argv += ["--render-png", args.render_png]
        if args.observer_view:
            sys.argv += ["--observer-view"]
        if args.edge_view:
            sys.argv += ["--edge-view", args.edge_view]
        sd.main()
        return 0

    raise SystemExit("Unknown command")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
