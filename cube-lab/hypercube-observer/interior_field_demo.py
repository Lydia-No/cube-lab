from __future__ import annotations

import argparse
import math
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import plotly.graph_objects as go

from cube_explorer.hypercube import Hypercube
from edge_memory import EdgeMemory, EdgeMode, Edge

Point3 = Tuple[float, float, float]


def vertex_to_point(vertex: int, dim: int) -> List[float]:
    bits = format(vertex, f"0{dim}b")
    return [1.0 if b == "1" else -1.0 for b in bits]


def project_4d_to_3d(p: List[float]) -> Point3:
    x, y, z, w = p
    scale = 1.0 / (2.0 - w)
    return (x * scale, y * scale, z * scale)


def to_point3(vertex: int, dim: int) -> Point3:
    p = vertex_to_point(vertex, dim)
    if dim == 3:
        return (p[0], p[1], p[2])
    if dim == 4:
        return project_4d_to_3d(p)
    return (p[0], p[1], p[2])


def _norm(p: Point3) -> float:
    return math.sqrt(p[0] * p[0] + p[1] * p[1] + p[2] * p[2])


def _normalize(p: Point3) -> Point3:
    n = _norm(p)
    if n <= 1e-12:
        return (0.0, 0.0, 0.0)
    return (p[0] / n, p[1] / n, p[2] / n)


def sphere_wireframe(radius: float = 1.0, rings: int = 10, segments: int = 40) -> go.Scatter3d:
    xs: List[float] = []
    ys: List[float] = []
    zs: List[float] = []
    for r in range(1, rings):
        theta = math.pi * r / rings
        for s in range(segments + 1):
            phi = 2.0 * math.pi * s / segments
            x = radius * math.sin(theta) * math.cos(phi)
            y = radius * math.sin(theta) * math.sin(phi)
            z = radius * math.cos(theta)
            xs.append(x)
            ys.append(y)
            zs.append(z)
        xs.append(None)
        ys.append(None)
        zs.append(None)

    for s in range(0, segments, max(1, segments // 8)):
        phi = 2.0 * math.pi * s / segments
        for r in range(rings + 1):
            theta = math.pi * r / rings
            x = radius * math.sin(theta) * math.cos(phi)
            y = radius * math.sin(theta) * math.sin(phi)
            z = radius * math.cos(theta)
            xs.append(x)
            ys.append(y)
            zs.append(z)
        xs.append(None)
        ys.append(None)
        zs.append(None)

    return go.Scatter3d(x=xs, y=ys, z=zs, mode="lines", line=dict(width=2), name="sky sphere")


@dataclass
class InteriorField:
    num_regions: int
    decay: float
    pulse: float
    clamp_max: float = 20.0

    def __post_init__(self) -> None:
        self.activation: List[float] = [0.0 for _ in range(self.num_regions)]

    def update(self, region: int) -> None:
        for i in range(self.num_regions):
            self.activation[i] *= self.decay
        self.activation[region] = min(self.clamp_max, self.activation[region] + self.pulse)


def _edges_to_segments(
    points: List[Point3],
    weights: Dict[Edge, float],
    min_weight: float,
) -> Tuple[List[float], List[float], List[float]]:
    ex: List[float] = []
    ey: List[float] = []
    ez: List[float] = []
    for (a, b), w in sorted(weights.items(), key=lambda kv: -kv[1]):
        if w < min_weight:
            continue
        p1 = points[a]
        p2 = points[b]
        ex += [p1[0], p2[0], None]
        ey += [p1[1], p2[1], None]
        ez += [p1[2], p2[2], None]
    return ex, ey, ez


def _write_png(fig: go.Figure, path: str, width: int, height: int, scale: float) -> None:
    try:
        fig.write_image(path, width=width, height=height, scale=scale)
    except Exception as e:
        raise RuntimeError(
            f"Failed to write PNG to '{path}'. Install kaleido: pip install -U kaleido. Error: {e}"
        ) from e


def _stable_jitter(v: int, seed: int, jitter: float) -> Point3:
    x = (1103515245 * (v + seed) + 12345) & 0x7FFFFFFF
    y = (1103515245 * (x + 1) + 12345) & 0x7FFFFFFF
    z = (1103515245 * (y + 1) + 12345) & 0x7FFFFFFF
    fx = (x / 0x7FFFFFFF) * 2.0 - 1.0
    fy = (y / 0x7FFFFFFF) * 2.0 - 1.0
    fz = (z / 0x7FFFFFFF) * 2.0 - 1.0
    return (fx * jitter, fy * jitter, fz * jitter)


def run_from_vertices(
    vertices: List[int],
    dim: int,
    activation_decay: float,
    activation_pulse: float,
    edge_mode: EdgeMode,
    edge_decay: float,
    fast_decay: float,
    slow_decay: float,
    consolidate_threshold: float,
    consolidate_amount: float,
    fast_min_weight: float,
    slow_min_weight: float,
    observer_view: bool,
    edge_view: str,
    region_depth: float,
    jitter: float,
    seed: int,
    pulse_boost: float,
    pulse_tau: float,
    save_html: Optional[str],
    save_png: Optional[str],
    png_width: int,
    png_height: int,
    png_scale: float,
) -> None:
    if not vertices:
        raise ValueError("vertices must be non-empty")

    num_regions = 1 << dim
    field = InteriorField(num_regions=num_regions, decay=activation_decay, pulse=activation_pulse)

    edges = EdgeMemory(
        num_regions=num_regions,
        mode=edge_mode,
        edge_decay=edge_decay,
        fast_decay=fast_decay,
        slow_decay=slow_decay,
        consolidate_threshold=consolidate_threshold,
        consolidate_amount=consolidate_amount,
    )

    last_seen: Dict[int, int] = defaultdict(lambda: -10**9)
    prev_v = int(vertices[0])

    for t, v in enumerate(vertices):
        v = int(v)
        field.update(v)
        last_seen[v] = t

        if t > 0:
            edges.step_decay()
            edges.add(prev_v, v, amount=1.0)
        prev_v = v

    base_points: List[Point3] = [to_point3(i, dim) for i in range(num_regions)]

    interior_points: List[Point3] = []
    for i, p in enumerate(base_points):
        jx, jy, jz = _stable_jitter(i, seed=seed, jitter=jitter)
        interior_points.append(
            (p[0] * region_depth + jx, p[1] * region_depth + jy, p[2] * region_depth + jz)
        )

    sky_points: List[Point3] = [_normalize(p) for p in interior_points]

    if observer_view:
        node_points = sky_points
        edge_points = sky_points if edge_view == "sky" else interior_points
    else:
        node_points = interior_points
        edge_points = interior_points

    xs = [p[0] for p in node_points]
    ys = [p[1] for p in node_points]
    zs = [p[2] for p in node_points]

    max_a = max(field.activation) if field.activation else 1.0
    sizes: List[float] = []
    t_final = len(vertices) - 1
    for i, a in enumerate(field.activation):
        base = 6.0 + 24.0 * (a / max_a)
        dt = max(0, t_final - last_seen[i])
        pulse = pulse_boost * math.exp(-dt / max(1e-6, pulse_tau))
        sizes.append(base + pulse)

    fast_ex, fast_ey, fast_ez = _edges_to_segments(edge_points, edges.fast, fast_min_weight)
    slow_ex, slow_ey, slow_ez = _edges_to_segments(edge_points, edges.slow, slow_min_weight)

    path_points_src = sky_points if observer_view else interior_points
    path_pts = [path_points_src[int(v)] for v in vertices]
    px = [p[0] for p in path_pts]
    py = [p[1] for p in path_pts]
    pz = [p[2] for p in path_pts]

    fig = go.Figure()

    if observer_view:
        fig.add_trace(sphere_wireframe(radius=1.0, rings=10, segments=40))

    fig.add_trace(
        go.Scatter3d(
            x=xs, y=ys, z=zs,
            mode="markers",
            marker=dict(size=sizes),
            name="regions (activation + pulse)",
        )
    )

    if fast_ex:
        fig.add_trace(
            go.Scatter3d(
                x=fast_ex, y=fast_ey, z=fast_ez,
                mode="lines",
                line=dict(width=2),
                name=f"fast edges (>= {fast_min_weight:g})",
            )
        )

    if slow_ex:
        fig.add_trace(
            go.Scatter3d(
                x=slow_ex, y=slow_ey, z=slow_ez,
                mode="lines",
                line=dict(width=6),
                name=f"slow backbone (>= {slow_min_weight:g})",
            )
        )

    fig.add_trace(
        go.Scatter3d(
            x=px, y=py, z=pz,
            mode="lines",
            line=dict(width=3),
            name="walk path",
        )
    )

    title = "Observer Sky" if observer_view else "Interior Volume"
    fig.update_layout(
        title=f"{title}: replayed walk (dim={dim}, steps={len(vertices)-1}, edge_view={edge_view})",
        scene=dict(
            xaxis=dict(range=[-1.8, 1.8]),
            yaxis=dict(range=[-1.8, 1.8]),
            zaxis=dict(range=[-1.8, 1.8]),
        ),
    )

    if save_html:
        fig.write_html(save_html)
    if save_png:
        _write_png(fig, save_png, width=png_width, height=png_height, scale=png_scale)

    fig.show()


def run(
    dim: int,
    steps: int,
    activation_decay: float,
    activation_pulse: float,
    edge_mode: EdgeMode,
    edge_decay: float,
    fast_decay: float,
    slow_decay: float,
    consolidate_threshold: float,
    consolidate_amount: float,
    fast_min_weight: float,
    slow_min_weight: float,
    observer_view: bool,
    edge_view: str,
    region_depth: float,
    jitter: float,
    seed: int,
    pulse_boost: float,
    pulse_tau: float,
    save_html: Optional[str],
    save_png: Optional[str],
    png_width: int,
    png_height: int,
    png_scale: float,
) -> None:
    cube = Hypercube(dim)
    _, vertices_raw = cube.random_walk(steps, return_vertices=True)
    vertices = [int(v) for v in vertices_raw]
    run_from_vertices(
        vertices=vertices,
        dim=dim,
        activation_decay=activation_decay,
        activation_pulse=activation_pulse,
        edge_mode=edge_mode,
        edge_decay=edge_decay,
        fast_decay=fast_decay,
        slow_decay=slow_decay,
        consolidate_threshold=consolidate_threshold,
        consolidate_amount=consolidate_amount,
        fast_min_weight=fast_min_weight,
        slow_min_weight=slow_min_weight,
        observer_view=observer_view,
        edge_view=edge_view,
        region_depth=region_depth,
        jitter=jitter,
        seed=seed,
        pulse_boost=pulse_boost,
        pulse_tau=pulse_tau,
        save_html=save_html,
        save_png=save_png,
        png_width=png_width,
        png_height=png_height,
        png_scale=png_scale,
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Interior field + observer view + hybrid connections demo")
    p.add_argument("--dim", type=int, default=3)
    p.add_argument("--steps", type=int, default=600)
    p.add_argument("--seed", type=int, default=1)

    p.add_argument("--activation-decay", type=float, default=0.995)
    p.add_argument("--activation-pulse", type=float, default=1.0)

    p.add_argument("--edge-mode", type=str, default="hybrid", choices=["persist", "decay", "hybrid"])
    p.add_argument("--edge-decay", type=float, default=0.995)
    p.add_argument("--fast-decay", type=float, default=0.990)
    p.add_argument("--slow-decay", type=float, default=0.9995)
    p.add_argument("--consolidate-threshold", type=float, default=8.0)
    p.add_argument("--consolidate-amount", type=float, default=4.0)

    p.add_argument("--fast-min-weight", type=float, default=2.0)
    p.add_argument("--slow-min-weight", type=float, default=3.0)

    p.add_argument("--observer-view", action="store_true")
    p.add_argument("--edge-view", type=str, default="sky", choices=["sky", "chord"])
    p.add_argument("--region-depth", type=float, default=0.75)
    p.add_argument("--jitter", type=float, default=0.05)

    p.add_argument("--pulse-boost", type=float, default=14.0)
    p.add_argument("--pulse-tau", type=float, default=35.0)

    p.add_argument("--save-html", type=str, default=None)
    p.add_argument("--save-png", type=str, default=None)
    p.add_argument("--png-width", type=int, default=1400)
    p.add_argument("--png-height", type=int, default=900)
    p.add_argument("--png-scale", type=float, default=2.0)

    args = p.parse_args()

    run(
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


if __name__ == "__main__":
    main()
