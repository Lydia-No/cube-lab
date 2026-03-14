class GrammarEvolution:
    """
    Tracks changes in learned symbolic operators over time.
    """

    def __init__(self):

        self.history = []

    def update(self, grammar):

        self.history.append(grammar.copy())

    def get_history(self):

        return self.history

    def print_evolution(self):

        for i, g in enumerate(self.history):

            print(f"\nGrammar snapshot {i}")

            for symbol, vec in g.items():

                print(symbol, "->", vec)
