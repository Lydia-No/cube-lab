class OperatorGrammar:
    """
    Maps symbols to transformation vectors.

    Example grammar:

    {
        "cave": (1,0,0),
        "horse": (0,1,0),
        "storm": (0,0,1)
    }
    """

    def __init__(self, grammar):

        if not isinstance(grammar, dict):
            raise ValueError("grammar must be a dictionary")

        self.grammar = grammar

    def symbols(self):

        return list(self.grammar.keys())

    def get_operator(self, symbol):

        if symbol not in self.grammar:
            raise ValueError(f"Unknown symbol: {symbol}")

        return self.grammar[symbol]

    def apply_sequence(self, cube, sequence):

        trajectory = [cube.get_state()]

        for symbol in sequence:

            operator = self.get_operator(symbol)

            cube.apply_vector(operator)

            trajectory.append(cube.get_state())

        return trajectory
