class RandomWalker:
    def __init__(self, cube):
        self.cube = cube

    def walk(self, steps):
        """
        Return:
        - path: visited vertices
        - symbols: emitted flip symbols
        """
        return self.cube.walk_with_path(steps)

    def symbols(self, steps):
        """
        Convenience method: return only symbolic sequence.
        """
        _, symbols = self.walk(steps)
        return symbols
