import random


class Hypercube:
    def __init__(self, dim: int):
        self.dim = dim

    def random_vertex(self) -> list[int]:
        return [random.randint(0, 1) for _ in range(self.dim)]

    def step(self, vertex: list[int]) -> tuple[list[int], int]:
        i = random.randrange(self.dim)
        new_vertex = vertex.copy()
        new_vertex[i] = 1 - new_vertex[i]
        return new_vertex, i

    def random_walk(self, steps: int) -> list[str]:
        _, symbols = self.walk_with_path(steps)
        return symbols

    def walk_with_path(self, steps: int) -> tuple[list[list[int]], list[str]]:
        vertex = self.random_vertex()
        path = [vertex.copy()]
        symbols: list[str] = []

        for _ in range(steps):
            vertex, dim = self.step(vertex)
            path.append(vertex.copy())
            symbols.append(chr(ord("A") + dim))

        return path, symbols
