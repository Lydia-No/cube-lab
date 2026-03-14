class AperiodicTile:

    def __init__(self, north, east, south, west, name):

        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.name = name

    def matches(self, other, direction):

        if direction == "east":
            return self.east == other.west

        if direction == "south":
            return self.south == other.north

        return False


class AperiodicTilingSystem:

    def __init__(self, tiles, size):

        self.tiles = tiles
        self.size = size
        self.grid = [[None]*size for _ in range(size)]

    def valid(self, x, y, tile):

        if x > 0 and self.grid[x-1][y]:
            if not self.grid[x-1][y].matches(tile, "east"):
                return False

        if y > 0 and self.grid[x][y-1]:
            if not self.grid[x][y-1].matches(tile, "south"):
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
