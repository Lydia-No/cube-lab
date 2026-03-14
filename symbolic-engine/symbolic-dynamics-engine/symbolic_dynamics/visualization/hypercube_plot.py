import networkx as nx
import plotly.graph_objects as go
import itertools


def build_hypercube_graph(n):

    G = nx.Graph()

    nodes = list(itertools.product([0,1], repeat=n))

    for v in nodes:
        G.add_node(v)

    for v in nodes:
        for i in range(n):

            u = list(v)
            u[i] ^= 1
            u = tuple(u)

            G.add_edge(v,u)

    return G


def plot_trajectory(G, trajectory):

    pos = nx.spring_layout(G, dim=3)

    node_x = []
    node_y = []
    node_z = []

    for node in G.nodes():
        x,y,z = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)

    edge_x = []
    edge_y = []
    edge_z = []

    for edge in G.edges():

        x0,y0,z0 = pos[edge[0]]
        x1,y1,z1 = pos[edge[1]]

        edge_x += [x0,x1,None]
        edge_y += [y0,y1,None]
        edge_z += [z0,z1,None]

    fig = go.Figure()

    fig.add_trace(go.Scatter3d(
        x=edge_x,
        y=edge_y,
        z=edge_z,
        mode='lines',
        line=dict(width=2,color='gray')
    ))

    traj_x=[]
    traj_y=[]
    traj_z=[]

    for node in trajectory:

        x,y,z = pos[node]

        traj_x.append(x)
        traj_y.append(y)
        traj_z.append(z)

    fig.add_trace(go.Scatter3d(
        x=traj_x,
        y=traj_y,
        z=traj_z,
        mode='lines+markers',
        marker=dict(size=6,color='red'),
        line=dict(width=4,color='red')
    ))

    fig.show()
