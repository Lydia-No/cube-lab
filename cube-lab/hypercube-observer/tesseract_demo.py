from cube_explorer.hypercube import Hypercube
import plotly.graph_objects as go


def vertex_to_point(vertex, dim):

    bits = format(vertex, f"0{dim}b")

    return [1 if b == "1" else -1 for b in bits]


def project_4d_to_3d(p):

    x,y,z,w = p

    scale = 1 / (2 - w)

    return (x*scale, y*scale, z*scale)


def run():

    dim = 4
    steps = 40

    cube = Hypercube(dim)

    seq, vertices = cube.random_walk(steps, return_vertices=True)

    points4 = [vertex_to_point(v, dim) for v in vertices]

    points3 = [project_4d_to_3d(p) for p in points4]

    xs = [p[0] for p in points3]
    ys = [p[1] for p in points3]
    zs = [p[2] for p in points3]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter3d(
            x=xs,
            y=ys,
            z=zs,
            mode="markers+lines",
            marker=dict(size=6,color="orange"),
            line=dict(width=4,color="red")
        )
    )

    fig.update_layout(
        title="Tesseract Walk (4D Cube Projection)",
        scene=dict(
            xaxis=dict(range=[-2,2]),
            yaxis=dict(range=[-2,2]),
            zaxis=dict(range=[-2,2])
        )
    )

    fig.show()


if __name__ == "__main__":
    run()
