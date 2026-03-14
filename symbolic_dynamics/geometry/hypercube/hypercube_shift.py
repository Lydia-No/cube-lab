import numpy as np


class HypercubeShift:

    def __init__(self, alphabet, dimension, size):

        self.alphabet = alphabet
        self.dimension = dimension
        self.size = size

        shape = tuple([size]*dimension)

        self.state = np.random.choice(alphabet, shape)

    def shift(self, axis):

        self.state = np.roll(self.state, 1, axis=axis)

    def show(self):

        print(self.state)
