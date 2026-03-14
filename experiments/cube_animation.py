from cube_explorer.hypercube import Hypercube
import plotly.graph_objects as go
from collections import defaultdict


def vertex_to_point(vertex, dim):
    bits = format(vertex, f"0{dim}b")
    return [1 if b == "1" else -1 for b in bits]


def cube_vertices():
    return [
        (-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),
        (1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)
    ]


def cube_edges():
    return [
        (0,1),(0,2),(0,4),
        (1,3),(1,5),
        (2,3),(2,6),
        (3,7),
        (4,5),(4,6),
        (5,7),
        (6,7)
    ]


def run():

    dim = 3
    steps = 80

    cube = Hypercube(dim)

    seq, vertices = cube.random_walk(steps, return_vertices=True)

    points = [vertex_to_point(v, dim) for v in vertices]

    visit_counts = defaultdict(int)
    transition_counts = defaultdict(int)

    cube_v = cube_vertices()
    edges = cube_edges()

    edge_x, edge_y, edge_z = [], [], []

    for e in edges:
        x0,y0,z0 = cube_v[e[0]]
        x1,y1,z1 = cube_v[e[1]]

        edge_x += [x0,x1,None]
        edge_y += [y0,y1,None]
        edge_z += [z0,z1,None]

    frames = []

    for i,p in enumerate(points):

        visit_counts[tuple(p)] += 1

        if i > 0:
            a = tuple(points[i-1])
            b = tuple(points[i])
            transition_counts[(a,b)] += 1

        visited_x, visited_y, visited_z, sizes = [],[],[],[]

        for point,count in visit_counts.items():
            visited_x.append(point[0])
            visited_y.append(point[1])
            visited_z.append(point[2])
            sizes.append(5 + count*3)

        edge_tx, edge_ty, edge_tz = [],[],[]

        for (a,b),count in transition_counts.items():

            if count < 2:
                continue

            edge_tx += [a[0],b[0],None]
            edge_ty += [a[1],b[1],None]
            edge_tz += [a[2],b[2],None]

        frames.append(
            go.Frame(
                data=[

                    go.Scatter3d(
                        x=visited_x,
                        y=visited_y,
                        z=visited_z,
                        mode="markers",
                        marker=dict(size=sizes,color="orange")
                    ),

                    go.Scatter3d(
                        x=edge_tx,
                        y=edge_ty,
                        z=edge_tz,
                        mode="lines",
                        line=dict(color="blue",width=3)
                    )

                ]
            )
        )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter3d(
            x=edge_x,
            y=edge_y,
            z=edge_z,
            mode='lines',
            line=dict(color='gray',width=2)
        )
    )

    fig.frames = frames

    fig.update_layout(
        title="Cube Network Growth",
        scene=dict(
            xaxis=dict(range=[-1.5,1.5]),
            yaxis=dict(range=[-1.5,1.5]),
            zaxis=dict(range=[-1.5,1.5]),
        ),
        updatemenus=[{
            "type":"buttons",
            "buttons":[
                {"label":"Play","method":"animate","args":[None]}
            ]
        }]
    )

    fig.show()

    for e in edges:
        x0,y0,z0 = cube_v[e[0]]
        x1,y1,z1 = cube_v[e[1]]

        edge_x += [x0,x1,None]
        edge_y += [y0,y1,None]
        edge_z += [z0,z1,None]

    frames = []

    visited_x, visited_y, visited_z, sizes = [],[],[],[]

    for i,p in enumerate(points):

        visit_counts[tuple(p)] += 1

        visited_x = []
        visited_y = []
        visited_z = []
        sizes = []

        for point,count in visit_counts.items():
            visited_x.append(point[0])
            visited_y.append(point[1])
            visited_z.append(point[2])
            sizes.append(5 + count*4)

        path_x = [pt[0] for pt in points[:i+1]]
        path_y = [pt[1] for pt in points[:i+1]]
        path_z = [pt[2] for pt in points[:i+1]]

        frames.append(
            go.Frame(
                data=[

                    go.Scatter3d(
                        x=visited_x,
                        y=visited_y,
                        z=visited_z,
                        mode="markers",
                        marker=dict(size=sizes,color="orange")
                    ),

                    go.Scatter3d(
                        x=path_x,
                        y=path_y,
                        z=path_z,
                        mode="lines",
                        line=dict(color="red",width=4)
                    )

                ]
            )
        )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter3d(
            x=edge_x,
            y=edge_y,
            z=edge_z,
            mode='lines',
            line=dict(color='gray',width=3)
        )
    )

    fig.add_trace(
        go.Scatter3d(
            x=[v[0] for v in cube_v],
            y=[v[1] for v in cube_v],
            z=[v[2] for v in cube_v],
            mode='markers',
            marker=dict(size=4,color='black')
        )
    )

    fig.frames = frames

    fig.update_layout(
        title="Cube Memory Field",
        scene=dict(
            xaxis=dict(range=[-1.5,1.5]),
            yaxis=dict(range=[-1.5,1.5]),
            zaxis=dict(range=[-1.5,1.5]),
        ),
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
