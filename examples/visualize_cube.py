import itertools
import plotly.graph_objects as go


def cube_vertices(dim=3):
    return list(itertools.product([0, 1], repeat=dim))


def cube_edges(vertices):
    edges = []

    for v in vertices:
        for i in range(len(v)):
            w = list(v)
            w[i] ^= 1
            w = tuple(w)

            if v < w:
                edges.append((v, w))

    return edges


def visualize_cube():

    vertices = cube_vertices(3)
    edges = cube_edges(vertices)

    x = [v[0] for v in vertices]
    y = [v[1] for v in vertices]
    z = [v[2] for v in vertices]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode="markers+text",
            text=[str(v) for v in vertices],
            textposition="top center",
            marker=dict(size=6),
        )
    )

    for v, w in edges:

        fig.add_trace(
            go.Scatter3d(
                x=[v[0], w[0]],
                y=[v[1], w[1]],
                z=[v[2], w[2]],
                mode="lines",
                line=dict(width=4),
            )
        )

    fig.update_layout(
        title="Hypercube Q3",
        scene=dict(
            xaxis_title="x",
            yaxis_title="y",
            zaxis_title="z",
        ),
    )

    fig.show()


if __name__ == "__main__":
    visualize_cube()

import random


def random_walk(vertices, steps=20):

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
