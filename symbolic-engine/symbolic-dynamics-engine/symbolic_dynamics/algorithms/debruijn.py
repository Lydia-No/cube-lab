import itertools
import networkx as nx


def debruijn_graph(alphabet, k):
    """
    Construct a De Bruijn graph of order k for given alphabet.
    Nodes are strings of length k-1
    Edges represent valid shifts.
    """

    G = nx.DiGraph()

    nodes = [''.join(p) for p in itertools.product(alphabet, repeat=k-1)]

    for node in nodes:
        for a in alphabet:

            new_word = node + a
            next_node = new_word[1:]

            G.add_edge(node, next_node, label=a)

    return G


def print_graph(G):

    print("Nodes:")
    for n in G.nodes:
        print(n)

    print("\nEdges:")
    for u, v, data in G.edges(data=True):
        print(u, "->", v, data["label"])
