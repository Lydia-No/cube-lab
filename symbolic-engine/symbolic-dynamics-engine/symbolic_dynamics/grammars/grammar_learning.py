from collections import defaultdict


class GrammarLearner:
    """
    Learns symbolic operators from state trajectories.
    """

    def __init__(self):

        self.symbol_vectors = {}

    def learn_from_sequence(self, sequence, trajectory):

        if len(sequence) + 1 != len(trajectory):
            raise ValueError("trajectory must be one longer than sequence")

        for i, symbol in enumerate(sequence):

            a = trajectory[i]
            b = trajectory[i + 1]

            vector = tuple(b[j] - a[j] for j in range(len(a)))

            if symbol not in self.symbol_vectors:

                self.symbol_vectors[symbol] = vector

        return self.symbol_vectors

    def get_grammar(self):

        return dict(self.symbol_vectors)
