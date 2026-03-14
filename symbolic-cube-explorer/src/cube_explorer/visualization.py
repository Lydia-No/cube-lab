import plotly.graph_objects as go


vertices={

0:(0,0,0),
1:(1,0,0),
2:(0,1,0),
3:(1,1,0),
4:(0,0,1),
5:(1,0,1),
6:(0,1,1),
7:(1,1,1)

}


edges=[

(0,1),(0,2),(0,4),
(1,3),(1,5),
(2,3),(2,6),
(3,7),
(4,5),(4,6),
(5,7),
(6,7)

]


def plot_cube_walk(path):

    fig = go.Figure()

    for e in edges:

        x=[vertices[e[0]][0],vertices[e[1]][0]]
        y=[vertices[e[0]][1],vertices[e[1]][1]]
        z=[vertices[e[0]][2],vertices[e[1]][2]]

        fig.add_trace(go.Scatter3d(x=x,y=y,z=z,mode="lines"))

    px=[vertices[v][0] for v in path]
    py=[vertices[v][1] for v in path]
    pz=[vertices[v][2] for v in path]

    fig.add_trace(go.Scatter3d(x=px,y=py,z=pz,mode="lines+markers"))

    return fig
