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
    steps = 60

    cube = Hypercube(dim)

    seq, vertices = cube.random_walk(steps, return_vertices=True)

    points = [vertex_to_point(v, dim) for v in vertices]

    visit_counts = defaultdict(int)
    transition_counts = defaultdict(int)

    cube_v = cube_vertices()
    edges = cube_edges()

    wire_x, wire_y, wire_z = [], [], []

    for e in edges:
        x0,y0,z0 = cube_v[e[0]]
        x1,y1,z1 = cube_v[e[1]]

        wire_x += [x0,x1,None]
        wire_y += [y0,y1,None]
        wire_z += [z0,z1,None]

    frames = []

    for i,p in enumerate(points):

        visit_counts[tuple(p)] += 1

        if i > 0:
            a = tuple(points[i-1])
            b = tuple(points[i])
            transition_counts[(a,b)] += 1

        node_x,node_y,node_z,node_size = [],[],[],[]

        for point,count in visit_counts.items():
            node_x.append(point[0])
            node_y.append(point[1])
            node_z.append(point[2])
            node_size.append(6 + count*2)

        edge_x,edge_y,edge_z = [],[],[]

        for (a,b),count in transition_counts.items():

            if count < 2:
                continue

            edge_x += [a[0],b[0],None]
            edge_y += [a[1],b[1],None]
            edge_z += [a[2],b[2],None]

        path = points[:i+1]

        path_x = [p[0] for p in path]
        path_y = [p[1] for p in path]
        path_z = [p[2] for p in path]

        frames.append(
            go.Frame(
                data=[

                    go.Scatter3d(
                        x=node_x,
                        y=node_y,
                        z=node_z,
                        mode='markers',
                        marker=dict(size=node_size,color='orange')
                    ),

                    go.Scatter3d(
                        x=edge_x,
                        y=edge_y,
                        z=edge_z,
                        mode='lines',
                        line=dict(color='blue',width=4)
                    ),

                    go.Scatter3d(
                        x=path_x,
                        y=path_y,
                        z=path_z,
                        mode='lines',
                        line=dict(color='red',width=4)
                    )

                ]
            )
        )

    fig = go.Figure()

    # static cube
    fig.add_trace(
        go.Scatter3d(
            x=wire_x,
            y=wire_y,
            z=wire_z,
            mode='lines',
            line=dict(color='gray',width=3)
        )
    )

    fig.frames = frames

    fig.update_layout(

        title="Cube Network Growth",

        scene=dict(
            xaxis=dict(range=[-1.5,1.5]),
            yaxis=dict(range=[-1.5,1.5]),
            zaxis=dict(range=[-1.5,1.5])
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
