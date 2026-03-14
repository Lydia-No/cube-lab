import numpy as np
from symbolic_dynamics.geometry.lattice.wang_rules import match_east, match_south


class WangSolver:

    def __init__(self, tiles, size):

        self.tiles = tiles
        self.size = size

        self.grid = np.empty((size, size), dtype=object)

    def valid(self, x, y, tile):

        if x > 0:

            left = self.grid[x-1][y]

            if left and not match_east(left, tile):
                return False

        if y > 0:

            above = self.grid[x][y-1]

            if above and not match_south(above, tile):
                return False

        return True

    def solve(self, x=0, y=0):

        if y == self.size:
            return True

        nx = x + 1
        ny = y

        if nx == self.size:
            nx = 0
            ny += 1

        for tile in self.tiles:

            if self.valid(x, y, tile):

                self.grid[x][y] = tile

                if self.solve(nx, ny):
                    return True

                self.grid[x][y] = None

        return False
