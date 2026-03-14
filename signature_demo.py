from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from cube_explorer.hypercube import Hypercube
from edge_memory import EdgeMemory, EdgeMode, Edge

Vertex = int
UndirEdge = Tuple[int, int]


def _undir(a: int, b: int) -> UndirEdge:
    return (a, b) if a <= b else (b, a)


def _entropy(probs: List[float]) -> float:
    h = 0.0
    for p in probs:
        if p > 0:
            h -= p * math.log(p + 1e-12)
    return h


def _bit_balance(vertices: List[Vertex], dim: int) -> List[float]:
    counts = [0] * dim
    for v in vertices:
        for b in range(dim):
            counts[b] += (v >> b) & 1
    n = max(1, len(vertices))
    return [c / n for c in counts]


def _octant_mass(vertices: List[Vertex], dim: int) -> Dict[str, float]:
    if dim < 3:
        return {}
    m: Dict[str, int] = {}
    for v in vertices:
        s = "".join("+" if ((v >> b) & 1) else "-" for b in range(3))
        m[s] = m.get(s, 0) + 1
    n = max(1, len(vertices))
    return {k: v / n for k, v in sorted(m.items())}


def _backbone_undirected(slow: Dict[Edge, float], min_w: float) -> Dict[UndirEdge, float]:
    out: Dict[UndirEdge, float] = {}
    for (a, b), w in slow.items():
        if w < min_w:
            continue
        e = _undir(a, b)
        out[e] = out.get(e, 0.0) + w
    return out


def _degree(undirected: Dict[UndirEdge, float]) -> Dict[int, int]:
    deg: Dict[int, int] = {}
    for (a, b) in undirected.keys():
        deg[a] = deg.get(a, 0) + 1
        deg[b] = deg.get(b, 0) + 1
    return deg


def _count_squares(undirected_edges: Set[UndirEdge]) -> int:
    adj: Dict[int, Set[int]] = {}
    for a, b in undirected_edges:
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)

    nodes = sorted(adj.keys())
    squares = 0
    for i, u in enumerate(nodes):
        nu = adj[u]
        for v in nodes[i + 1 :]:
            k = len(nu & adj[v])
            if k >= 2:
                squares += k * (k - 1) // 2
    return squares // 2


def _jaccard(a: Set[UndirEdge], b: Set[UndirEdge]) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / max(1, len(a | b))


def timeline_from_vertices(
    vertices: List[Vertex],
    dim: int,
    slow_min_weight: float,
    window: int = 200,
    stable_jaccard: float = 0.90,
    stable_windows: int = 3,
) -> Dict[str, Optional[int]]:
    em = EdgeMemory(
        num_regions=1 << dim,
        mode=EdgeMode.HYBRID,
        edge_decay=0.995,
        fast_decay=0.990,
        slow_decay=0.9995,
        consolidate_threshold=8.0,
        consolidate_amount=4.0,
    )

    first_edge_t: Optional[int] = None
    first_square_t: Optional[int] = None

    prev_set: Set[UndirEdge] = set()
    stable_run = 0
    stabilization_t: Optional[int] = None

    prev = vertices[0]
    for t, v in enumerate(vertices[1:], start=1):
        em.step_decay()
        em.add(prev, v, amount=1.0)
        prev = v

        bb = _backbone_undirected(em.slow, slow_min_weight)
        bb_set = set(bb.keys())

        if first_edge_t is None and bb_set:
            first_edge_t = t

        if first_square_t is None and bb_set and _count_squares(bb_set) > 0:
            first_square_t = t

        if t % window == 0:
            j = _jaccard(prev_set, bb_set)
            if j >= stable_jaccard:
                stable_run += 1
                if stabilization_t is None and stable_run >= stable_windows:
                    stabilization_t = t
            else:
                stable_run = 0
            prev_set = bb_set

    return {
        "first_backbone_edge_time": first_edge_t,
        "first_square_time": first_square_t,
        "stabilization_time": stabilization_t,
    }


@dataclass(frozen=True)
class Signature:
    dim: int
    steps: int
    bit_balance: List[float]
    bit_balance_entropy: float
    octant_mass: Dict[str, float]
    backbone_edges: int
    backbone_squares: int
    backbone_max_degree: int
    backbone_degree_hist: Dict[str, int]
    timeline: Dict[str, Optional[int]]
    top_backbone_edges: List[Tuple[str, float]]

    def to_json(self) -> Dict[str, object]:
        return {
            "dim": self.dim,
            "steps": self.steps,
            "bit_balance": self.bit_balance,
            "bit_balance_entropy": self.bit_balance_entropy,
            "octant_mass": self.octant_mass,
            "backbone_edges": self.backbone_edges,
            "backbone_squares": self.backbone_squares,
            "backbone_max_degree": self.backbone_max_degree,
            "backbone_degree_hist": self.backbone_degree_hist,
            "timeline": self.timeline,
            "top_backbone_edges": self.top_backbone_edges,
        }


def signature_from_walk(dim: int, steps: int, seed: int, slow_min_weight: float, top_edges: int) -> Signature:
    cube = Hypercube(dim)
    _, vertices_raw = cube.random_walk(steps, return_vertices=True)
    vertices = [int(v) for v in vertices_raw]

    bb = _bit_balance(vertices, dim)
    h = _entropy([p for p in bb] + [1 - p for p in bb]) / max(1, 2 * dim)

    em = EdgeMemory(
        num_regions=1 << dim,
        mode=EdgeMode.HYBRID,
        edge_decay=0.995,
        fast_decay=0.990,
        slow_decay=0.9995,
        consolidate_threshold=8.0,
        consolidate_amount=4.0,
    )
    prev = vertices[0]
    for v in vertices[1:]:
        em.step_decay()
        em.add(prev, v, amount=1.0)
        prev = v

    bb_undir = _backbone_undirected(em.slow, min_w=slow_min_weight)
    bb_edges = set(bb_undir.keys())
    deg = _degree(bb_undir)
    max_deg = max(deg.values()) if deg else 0
    hist: Dict[int, int] = {}
    for d in deg.values():
        hist[d] = hist.get(d, 0) + 1
    hist_str = {str(k): v for k, v in sorted(hist.items())}

    squares = _count_squares(bb_edges)
    top = sorted(bb_undir.items(), key=lambda kv: kv[1], reverse=True)[:top_edges]
    top_fmt = [(f"({a},{b})", float(w)) for (a, b), w in top]

    tl = timeline_from_vertices(vertices, dim=dim, slow_min_weight=slow_min_weight)

    return Signature(
        dim=dim,
        steps=steps,
        bit_balance=bb,
        bit_balance_entropy=float(h),
        octant_mass=_octant_mass(vertices, dim),
        backbone_edges=len(bb_edges),
        backbone_squares=int(squares),
        backbone_max_degree=int(max_deg),
        backbone_degree_hist=hist_str,
        timeline=tl,
        top_backbone_edges=top_fmt,
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Signatures for interior/backbone geometry (with timeline).")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("signature", help="Print one signature JSON.")
    s.add_argument("--dim", type=int, default=3)
    s.add_argument("--steps", type=int, default=2000)
    s.add_argument("--seed", type=int, default=1)
    s.add_argument("--slow-min-weight", type=float, default=3.0)
    s.add_argument("--top-edges", type=int, default=20)

    c = sub.add_parser("cluster", help="Generate many signatures and bucket them.")
    c.add_argument("--n", type=int, default=50)
    c.add_argument("--dim", type=int, default=3)
    c.add_argument("--steps", type=int, default=2000)
    c.add_argument("--seed0", type=int, default=1)
    c.add_argument("--slow-min-weight", type=float, default=3.0)
    c.add_argument("--top-edges", type=int, default=20)

    args = p.parse_args()

    if args.cmd == "signature":
        sig = signature_from_walk(
            dim=args.dim,
            steps=args.steps,
            seed=args.seed,
            slow_min_weight=args.slow_min_weight,
            top_edges=args.top_edges,
        )
        print(json.dumps(sig.to_json(), indent=2))
        return

    # cluster: coarse bucketing by timeline + squares + max_degree
    buckets: Dict[Tuple[Optional[int], Optional[int], int, int], int] = {}
    for i in range(args.n):
        sig = signature_from_walk(
            dim=args.dim,
            steps=args.steps,
            seed=args.seed0 + i,
            slow_min_weight=args.slow_min_weight,
            top_edges=args.top_edges,
        )
        key = (
            sig.timeline.get("first_backbone_edge_time"),
            sig.timeline.get("first_square_time"),
            sig.backbone_squares,
            sig.backbone_max_degree,
        )
        buckets[key] = buckets.get(key, 0) + 1

    summary = [{"bucket": list(map(lambda x: x if x is not None else -1, k)), "count": v} for k, v in buckets.items()]
    summary.sort(key=lambda d: d["count"], reverse=True)
    print(json.dumps({"buckets_top20": summary[:20]}, indent=2))


if __name__ == "__main__":
    main()
