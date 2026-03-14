class SymbolicWalker:
    """
    Executes symbolic sequences on a state space.
    """

    def __init__(self, cube, grammar):

        self.cube = cube
        self.grammar = grammar

    def run(self, sequence):

        trajectory = [self.cube.get_state()]

        for symbol in sequence:

            if symbol not in self.grammar:
                raise ValueError(f"Unknown symbol: {symbol}")

            operator = self.grammar[symbol]

            self.cube.apply_vector(operator)

            trajectory.append(self.cube.get_state())

        return trajectory
