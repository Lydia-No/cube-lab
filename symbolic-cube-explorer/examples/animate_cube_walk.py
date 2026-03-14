import itertools
import random
import plotly.graph_objects as go


def cube_vertices():
    return list(itertools.product([0, 1], repeat=3))


def cube_edges(vertices):
    edges = []

    for v in vertices:
        for i in range(3):
            w = list(v)
            w[i] ^= 1
            w = tuple(w)

            if v < w:
                edges.append((v, w))

    return edges


def neighbors(v):
    n = []

    for i in range(3):
        w = list(v)
        w[i] ^= 1
        n.append(tuple(w))

    return n


def random_walk(vertices, steps=25):

    current = random.choice(vertices)

    path = [current]

    for _ in range(steps):

        current = random.choice(neighbors(current))

        path.append(current)

    return path


def animate():

    vertices = cube_vertices()
    edges = cube_edges(vertices)

    path = random_walk(vertices, 30)

    fig = go.Figure()

    # cube vertices
    x = [v[0] for v in vertices]
    y = [v[1] for v in vertices]
    z = [v[2] for v in vertices]

    fig.add_trace(
        go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode="markers+text",
            text=[str(v) for v in vertices],
            marker=dict(size=5)
        )
    )

    # cube edges
    for v, w in edges:

        fig.add_trace(
            go.Scatter3d(
                x=[v[0], w[0]],
                y=[v[1], w[1]],
                z=[v[2], w[2]],
                mode="lines",
                line=dict(width=3)
            )
        )

    frames = []

    for i in range(1, len(path)):

        v = path[i]

        frames.append(
            go.Frame(
                data=[
                    go.Scatter3d(
                        x=[v[0]],
                        y=[v[1]],
                        z=[v[2]],
                        mode="markers",
                        marker=dict(size=10)
                    )
                ]
            )
        )

    fig.frames = frames

    fig.add_trace(
        go.Scatter3d(
            x=[path[0][0]],
            y=[path[0][1]],
            z=[path[0][2]],
            mode="markers",
            marker=dict(size=10)
        )
    )

    fig.update_layout(
        title="Animated Hypercube Walker",
        updatemenus=[
            dict(
                type="buttons",
                buttons=[
                    dict(
                        label="Play",
                        method="animate",
                        args=[None]
                    )
                ]
            )
        ]
    )

    fig.show()


if __name__ == "__main__":
    animate()
