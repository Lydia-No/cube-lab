import networkx as nx
import plotly.graph_objects as go
from cube_explorer.hypercube import Hypercube


def build_transition_graph(sequence):

    G = nx.DiGraph()

    for i in range(len(sequence) - 1):

        a = sequence[i]
        b = sequence[i + 1]

        if G.has_edge(a, b):
            G[a][b]["weight"] += 1
        else:
            G.add_edge(a, b, weight=1)

    return G


def plot_graph(G):

    pos = nx.spring_layout(G)

    edge_x = []
    edge_y = []

    for edge in G.edges():

        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(width=2),
        hoverinfo="none"
    )

    node_x = []
    node_y = []

    for node in G.nodes():

        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=list(G.nodes()),
        textposition="top center",
        marker=dict(size=20)
    )

    fig = go.Figure(data=[edge_trace, node_trace])

    fig.update_layout(
        title="Symbol Transition Graph",
        showlegend=False
    )

    fig.show()


def run(dim=4, steps=10000):

    cube = Hypercube(dim)

    seq = cube.random_walk(steps)

    G = build_transition_graph(seq)

    plot_graph(G)


if __name__ == "__main__":

    run(dim=6, steps=20000)
