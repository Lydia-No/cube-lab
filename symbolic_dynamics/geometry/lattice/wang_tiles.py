class WangTile:

    def __init__(self, north, east, south, west):

        self.north = north
        self.east = east
        self.south = south
        self.west = west


def valid_adjacent(tile1, tile2):

    return tile1.east == tile2.west
