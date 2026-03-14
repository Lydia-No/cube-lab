from cube_explorer.hypercube import Hypercube
import plotly.graph_objects as go
import math
from collections import defaultdict


def vertex_to_point(vertex, dim):
    bits = format(vertex, f"0{dim}b")
    return [1 if b == "1" else -1 for b in bits]


def project_4d_to_3d(p):
    x, y, z, w = p
    scale = 1 / (2 - w)
    return (x * scale, y * scale, z * scale)


def to_sky(p):
    x, y, z = p
    r = math.sqrt(x*x + y*y + z*z)
    az = math.degrees(math.atan2(y, x))
    el = math.degrees(math.asin(z / r))
    return az, el


def run():

    dim = 4
    steps = 80

    cube = Hypercube(dim)

    seq, vertices = cube.random_walk(steps, return_vertices=True)

    visit_counts = defaultdict(int)
    transitions = defaultdict(int)

    prev = None

    frames = []

    for v in vertices:

        p4 = vertex_to_point(v, dim)
        p3 = project_4d_to_3d(p4)

        visit_counts[p3] += 1

        if prev is not None:
            transitions[(prev, p3)] += 1

        prev = p3

        star_x = []
        star_y = []
        sizes = []

        for p, count in visit_counts.items():

            az, el = to_sky(p)

            star_x.append(az)
            star_y.append(el)

            sizes.append(6 + count*3)

        line_x = []
        line_y = []

        for (a, b), count in transitions.items():

            if count < 2:
                continue

            az1, el1 = to_sky(a)
            az2, el2 = to_sky(b)

            line_x += [az1, az2, None]
            line_y += [el1, el2, None]

        frames.append(
            go.Frame(
                data=[

                    go.Scatter(
                        x=star_x,
                        y=star_y,
                        mode="markers",
                        marker=dict(size=sizes, color="orange")
                    ),

                    go.Scatter(
                        x=line_x,
                        y=line_y,
                        mode="lines",
                        line=dict(color="blue", width=2)
                    )

                ]
            )
        )

    fig = go.Figure()

    fig.frames = frames

    fig.update_layout(

        title="Evolving Symbolic Sky",

        xaxis=dict(range=[-180,180], title="Azimuth"),
        yaxis=dict(range=[-90,90], title="Elevation"),

        updatemenus=[{
            "type":"buttons",
            "buttons":[
                {"label":"Play","method":"animate","args":[None]}
            ]
        }]
    )

    fig.show()


if __name__ == "__main__":
    run()
