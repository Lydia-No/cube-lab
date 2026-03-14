from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from cube_explorer.hypercube import Hypercube
from edge_memory import EdgeMemory, EdgeMode, Edge

Vertex = int


def jaccard(a: Set[Edge], b: Set[Edge]) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / max(1, len(a | b))


def backbone_ratio(weights: Dict[Edge, float], k: int) -> float:
    if not weights:
        return 0.0
    total = sum(weights.values())
    if total <= 0:
        return 0.0
    topk = sum(w for _, w in sorted(weights.items(), key=lambda kv: kv[1], reverse=True)[:k])
    return topk / total


@dataclass(frozen=True)
class WindowRow:
    end_t: int
    morph_fast: float
    morph_slow: float
    active_fast: int
    active_slow: int
    backbone_fast: float
    backbone_slow: float


def run_metrics(
    dim: int,
    steps: int,
    window: int,
    edge_mode: EdgeMode,
    edge_decay: float,
    fast_decay: float,
    slow_decay: float,
    consolidate_threshold: float,
    consolidate_amount: float,
    active_threshold_fast: float,
    active_threshold_slow: float,
    backbone_k: int,
) -> List[WindowRow]:
    cube = Hypercube(dim)
    _, vertices_raw = cube.random_walk(steps, return_vertices=True)
    vertices: List[Vertex] = [int(v) for v in vertices_raw]

    num_regions = 1 << dim
    edges = EdgeMemory(
        num_regions=num_regions,
        mode=edge_mode,
        edge_decay=edge_decay,
        fast_decay=fast_decay,
        slow_decay=slow_decay,
        consolidate_threshold=consolidate_threshold,
        consolidate_amount=consolidate_amount,
    )

    prev_v = vertices[0]

    prev_fast: Set[Edge] = set()
    prev_slow: Set[Edge] = set()
    rows: List[WindowRow] = []

    for t, v in enumerate(vertices[1:], start=1):
        edges.step_decay()
        edges.add(prev_v, v, amount=1.0)
        prev_v = v

        if t % window == 0:
            fast_active = {e for e, w in edges.fast.items() if w >= active_threshold_fast}
            slow_active = {e for e, w in edges.slow.items() if w >= active_threshold_slow}

            rows.append(
                WindowRow(
                    end_t=t,
                    morph_fast=jaccard(prev_fast, fast_active),
                    morph_slow=jaccard(prev_slow, slow_active),
                    active_fast=len(fast_active),
                    active_slow=len(slow_active),
                    backbone_fast=backbone_ratio(edges.fast, backbone_k),
                    backbone_slow=backbone_ratio(edges.slow, backbone_k),
                )
            )
            prev_fast = fast_active
            prev_slow = slow_active

    return rows


def print_table(rows: List[WindowRow]) -> None:
    if not rows:
        print("No rows (increase steps or reduce window).")
        return

    header = (
        "end_t | morph_fast | morph_slow | active_fast | active_slow | "
        "backbone_fast | backbone_slow"
    )
    print(header)
    print("-" * len(header))
    for r in rows:
        print(
            f"{r.end_t:5d} | "
            f"{r.morph_fast:9.3f} | {r.morph_slow:9.3f} | "
            f"{r.active_fast:11d} | {r.active_slow:11d} | "
            f"{r.backbone_fast:13.3f} | {r.backbone_slow:13.3f}"
        )


def main() -> None:
    p = argparse.ArgumentParser(description="Windowed metrics for hybrid edge memory.")
    p.add_argument("--dim", type=int, default=3)
    p.add_argument("--steps", type=int, default=5000)
    p.add_argument("--window", type=int, default=200)

    p.add_argument("--edge-mode", type=str, default="hybrid", choices=["persist", "decay", "hybrid"])
    p.add_argument("--edge-decay", type=float, default=0.995)

    p.add_argument("--fast-decay", type=float, default=0.990)
    p.add_argument("--slow-decay", type=float, default=0.9995)
    p.add_argument("--consolidate-threshold", type=float, default=8.0)
    p.add_argument("--consolidate-amount", type=float, default=4.0)

    p.add_argument("--active-threshold-fast", type=float, default=1.0)
    p.add_argument("--active-threshold-slow", type=float, default=1.0)
    p.add_argument("--backbone-k", type=int, default=10)

    args = p.parse_args()

    rows = run_metrics(
        dim=args.dim,
        steps=args.steps,
        window=args.window,
        edge_mode=EdgeMode(args.edge_mode),
        edge_decay=args.edge_decay,
        fast_decay=args.fast_decay,
        slow_decay=args.slow_decay,
        consolidate_threshold=args.consolidate_threshold,
        consolidate_amount=args.consolidate_amount,
        active_threshold_fast=args.active_threshold_fast,
        active_threshold_slow=args.active_threshold_slow,
        backbone_k=args.backbone_k,
    )
    print_table(rows)


if __name__ == "__main__":
    main()
