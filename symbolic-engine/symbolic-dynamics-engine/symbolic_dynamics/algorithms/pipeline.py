import networkx as nx
import numpy as np
from symbolic_dynamics.algorithms.sft_matrix import build_sft_matrix
from symbolic_dynamics.algorithms.topological_entropy import topological_entropy


class SFTPipeline:

    def __init__(self, alphabet, forbidden):

        self.alphabet = alphabet
        self.forbidden = forbidden

    def build_graph(self):

        A, states = build_sft_matrix(self.alphabet, self.forbidden)

        G = nx.DiGraph()

        for i in range(len(states)):
            for j in range(len(states)):
                if A[i][j] == 1:
                    G.add_edge(states[i], states[j])

        return G, A

    def entropy(self):

        _, A = self.build_graph()

        return topological_entropy(A)
