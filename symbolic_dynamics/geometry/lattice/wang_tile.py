class WangTile:

    def __init__(self, north, east, south, west, name="tile"):

        self.north = north
        self.east = east
        self.south = south
        self.west = west

        self.name = name

    def __repr__(self):

        return f"{self.name}({self.north},{self.east},{self.south},{self.west})"
