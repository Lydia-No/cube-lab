from cube_explorer.hypercube import Hypercube
import plotly.graph_objects as go


def vertex_to_point(vertex, dim):
    bits = format(vertex, f"0{dim}b")
    return [1 if b == "1" else -1 for b in bits]


def run():

    dim = 3
    steps = 20

    cube = Hypercube(dim)

    seq, vertices = cube.random_walk(steps, return_vertices=True)

    points = [vertex_to_point(v, dim) for v in vertices]

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    zs = [p[2] for p in points]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter3d(
            x=xs,
            y=ys,
            z=zs,
            mode="markers+lines",
            marker=dict(size=6),
            line=dict(width=4)
        )
    )

    fig.update_layout(
        title="Cube Walk",
        scene=dict(
            xaxis=dict(range=[-1.5,1.5]),
            yaxis=dict(range=[-1.5,1.5]),
            zaxis=dict(range=[-1.5,1.5])
        )
    )

    fig.show()


if __name__ == "__main__":
    run()
