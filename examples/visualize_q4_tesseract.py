import itertools
import plotly.graph_objects as go

import random

def vertices(dim):
    return list(itertools.product([0, 1], repeat=dim))


def edges(vertices):
    e = []

    for v in vertices:
        for i in range(len(v)):
            w = list(v)
            w[i] ^= 1
            w = tuple(w)

            if v < w:
                e.append((v, w))

    return e


def project_4d_to_3d(v):
    x, y, z, w = v

    scale = 1 + w * 0.6

    return (
        x * scale,
        y * scale,
        z * scale,
    )

def random_walk(vertices, steps=40):

    current = random.choice(vertices)

    path = [current]

    for _ in range(steps):

        neighbors = []

        for i in range(len(current)):
            w = list(current)
            w[i] ^= 1
            neighbors.append(tuple(w))

        current = random.choice(neighbors)

        path.append(current)

    return path

def visualize():

    verts4 = vertices(4)
    ed = edges(verts4)

    projected = [project_4d_to_3d(v) for v in verts4]

    x = [p[0] for p in projected]
    y = [p[1] for p in projected]
    z = [p[2] for p in projected]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode="markers+text",
            text=[str(v) for v in verts4],
            textposition="top center",
            marker=dict(size=5),
        )
    )

    for v, w in ed:

        p1 = project_4d_to_3d(v)
        p2 = project_4d_to_3d(w)

        fig.add_trace(
            go.Scatter3d(
                x=[p1[0], p2[0]],
                y=[p1[1], p2[1]],
                z=[p1[2], p2[2]],
                mode="lines",
                line=dict(width=4),
            )
        )

    fig.update_layout(
        title="Q4 Hypercube (Tesseract Projection)"
    )

    fig.show()


if __name__ == "__main__":
    visualize()
