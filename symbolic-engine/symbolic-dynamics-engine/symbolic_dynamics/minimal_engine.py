import itertools
import math
import numpy as np
import networkx as nx


class Subshift:
    """
    Subshift defined by forbidden words.
    """

    def __init__(self, alphabet, forbidden=None):

        self.alphabet = list(alphabet)
        self.forbidden = set(forbidden or [])

    def allowed(self, word):

        word = "".join(word)

        for f in self.forbidden:
            if f in word:
                return False

        return True

    def words(self, n):
        """
        Generate all allowed words of length n.
        """

        results = []

        for w in itertools.product(self.alphabet, repeat=n):

            if self.allowed(w):
                results.append("".join(w))

        return results

    def word_growth(self, n):
        """
        |L_n| number of allowed words of length n
        """

        return len(self.words(n))

    def entropy_estimate(self, n=8):
        """
        Estimate entropy via word growth.
        """

        counts = []

        for k in range(1, n + 1):
            counts.append(self.word_growth(k))

        ratios = []

        for k in range(1, len(counts)):
            ratios.append(math.log(counts[k]) - math.log(counts[k - 1]))

        return sum(ratios) / len(ratios)

    def transition_graph(self, k=2):
        """
        Construct k-block transition graph.
        """

        nodes = self.words(k)

        G = nx.DiGraph()

        for w in nodes:
            G.add_node(w)

        for w in nodes:
            for a in self.alphabet:

                candidate = w[1:] + a

                if self.allowed(candidate):
                    G.add_edge(w, candidate)

        return G

    def adjacency_matrix(self, k=2):

        G = self.transition_graph(k)

        nodes = list(G.nodes())

        A = np.zeros((len(nodes), len(nodes)))

        for i, u in enumerate(nodes):
            for j, v in enumerate(nodes):

                if G.has_edge(u, v):
                    A[i, j] = 1

        return A

    def entropy_matrix(self, k=2):

        A = self.adjacency_matrix(k)

        eigs = np.linalg.eigvals(A)

        lam = max(abs(eigs))

        return math.log(lam)
