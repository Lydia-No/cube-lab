import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(G):

    pos = nx.spring_layout(G)

    labels = nx.get_edge_attributes(G, 'label')

    nx.draw(G, pos, with_labels=True)

    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.show()
