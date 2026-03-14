from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

from edge_memory import EdgeMemory, EdgeMode, Edge

Vertex = int
Action = int
UndirEdge = Tuple[int, int]


def _undir(a: int, b: int) -> UndirEdge:
    return (a, b) if a <= b else (b, a)


def actions_to_vertices(dim: int, actions: List[Action], start: int = 0) -> List[Vertex]:
    v = start
    verts = [v]
    for a in actions:
        v ^= (1 << a)
        verts.append(v)
    return verts


def _build_slow_backbone(vertices: List[Vertex], dim: int, slow_min_weight: float) -> Dict[UndirEdge, float]:
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

    out: Dict[UndirEdge, float] = {}
    for (a, b), w in em.slow.items():
        if w < slow_min_weight:
            continue
        e = _undir(a, b)
        out[e] = out.get(e, 0.0) + w
    return out


def _degree(edges: Dict[UndirEdge, float]) -> Dict[int, int]:
    deg: Dict[int, int] = {}
    for a, b in edges.keys():
        deg[a] = deg.get(a, 0) + 1
        deg[b] = deg.get(b, 0) + 1
    return deg


def _count_squares(edges_set: set[UndirEdge]) -> int:
    adj: Dict[int, set[int]] = {}
    for a, b in edges_set:
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


def score_motif(backbone: Dict[UndirEdge, float], motif: str) -> float:
    edges_set = set(backbone.keys())
    deg = _degree(backbone)
    max_deg = max(deg.values()) if deg else 0
    squares = _count_squares(edges_set)

    if motif == "square":
        return 10.0 * squares + 0.1 * len(edges_set)
    if motif == "hub":
        return 2.0 * max_deg + 0.05 * len(edges_set)
    if motif == "bridge":
        return 3.0 * (1.0 / max(1, len(edges_set))) + 0.2 * max_deg
    if motif == "two_cycle":
        return (max(backbone.values()) if backbone else 0.0) - 0.05 * len(edges_set)
    raise ValueError(f"Unknown motif: {motif}")


@dataclass
class Candidate:
    actions: List[Action]
    score: float
    backbone_edges: int
    backbone_squares: int
    backbone_max_degree: int


def eval_actions(dim: int, actions: List[Action], slow_min_weight: float) -> Candidate:
    verts = actions_to_vertices(dim, actions)
    bb = _build_slow_backbone(verts, dim=dim, slow_min_weight=slow_min_weight)
    deg = _degree(bb)
    max_deg = max(deg.values()) if deg else 0
    squares = _count_squares(set(bb.keys()))
    sc = score_motif(bb, motif=args_motif_global)  # set by main()
    return Candidate(
        actions=list(actions),
        score=sc,
        backbone_edges=len(bb),
        backbone_squares=squares,
        backbone_max_degree=max_deg,
    )


args_motif_global = "square"


def search(
    dim: int,
    steps: int,
    motif: str,
    iters: int,
    restarts: int,
    slow_min_weight: float,
    seed: int,
) -> Candidate:
    global args_motif_global
    args_motif_global = motif

    rng = random.Random(seed)
    best = Candidate(actions=[], score=-1e18, backbone_edges=0, backbone_squares=0, backbone_max_degree=0)

    for _r in range(restarts):
        actions = [rng.randrange(dim) for _ in range(steps)]
        cand = eval_actions(dim, actions, slow_min_weight=slow_min_weight)
        if cand.score > best.score:
            best = cand

        for _ in range(iters):
            trial = list(actions)
            m = 1 + rng.randrange(3)
            for __ in range(m):
                idx = rng.randrange(steps)
                trial[idx] = rng.randrange(dim)

            tc = eval_actions(dim, trial, slow_min_weight=slow_min_weight)
            if tc.score >= cand.score:
                actions = trial
                cand = tc
                if cand.score > best.score:
                    best = cand

    return best


def maybe_render(
    dim: int,
    actions: List[Action],
    render_html: Optional[str],
    render_png: Optional[str],
    observer_view: bool,
    edge_view: str,
    seed: int,
) -> None:
    if not render_html and not render_png:
        return

    import interior_field_demo as demo

    vertices = actions_to_vertices(dim, actions)

    demo.run_from_vertices(
        vertices=vertices,
        dim=dim,
        activation_decay=0.995,
        activation_pulse=1.0,
        edge_mode=EdgeMode.HYBRID,
        edge_decay=0.995,
        fast_decay=0.990,
        slow_decay=0.9995,
        consolidate_threshold=8.0,
        consolidate_amount=4.0,
        fast_min_weight=2.0,
        slow_min_weight=3.0,
        observer_view=observer_view,
        edge_view=edge_view,
        region_depth=0.75,
        jitter=0.05,
        seed=seed,
        pulse_boost=14.0,
        pulse_tau=35.0,
        save_html=render_html,
        save_png=render_png,
        png_width=1400,
        png_height=900,
        png_scale=2.0,
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Synthesize a walk that produces a target motif in the slow backbone.")
    p.add_argument("--dim", type=int, default=3)
    p.add_argument("--steps", type=int, default=700)
    p.add_argument("--motif", type=str, default="square", choices=["square", "hub", "bridge", "two_cycle"])
    p.add_argument("--iters", type=int, default=500)
    p.add_argument("--restarts", type=int, default=12)
    p.add_argument("--slow-min-weight", type=float, default=3.0)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--out-actions", type=str, default="best_actions.json")

    # Auto-render (A)
    p.add_argument("--render-html", type=str, default=None)
    p.add_argument("--render-png", type=str, default=None)
    p.add_argument("--observer-view", action="store_true")
    p.add_argument("--edge-view", type=str, default="sky", choices=["sky", "chord"])

    args = p.parse_args()

    best = search(
        dim=args.dim,
        steps=args.steps,
        motif=args.motif,
        iters=args.iters,
        restarts=args.restarts,
        slow_min_weight=args.slow_min_weight,
        seed=args.seed,
    )

    out = {
        "dim": args.dim,
        "steps": args.steps,
        "motif": args.motif,
        "score": best.score,
        "backbone_edges": best.backbone_edges,
        "backbone_squares": best.backbone_squares,
        "backbone_max_degree": best.backbone_max_degree,
        "actions_head": best.actions[:30],
    }
    print(json.dumps(out, indent=2))

    if args.out_actions:
        with open(args.out_actions, "w", encoding="utf-8") as f:
            json.dump(best.actions, f)

    maybe_render(
        dim=args.dim,
        actions=best.actions,
        render_html=args.render_html,
        render_png=args.render_png,
        observer_view=args.observer_view,
        edge_view=args.edge_view,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
