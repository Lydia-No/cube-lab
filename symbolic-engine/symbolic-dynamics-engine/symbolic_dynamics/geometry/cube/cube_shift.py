import numpy as np


class CubeShift:

    def __init__(self, alphabet, size):

        self.alphabet = alphabet
        self.size = size

        self.state = np.random.choice(alphabet, (size, size, size))

    def shift_x(self):

        self.state = np.roll(self.state, 1, axis=0)

    def shift_y(self):

        self.state = np.roll(self.state, 1, axis=1)

    def shift_z(self):

        self.state = np.roll(self.state, 1, axis=2)

    def show(self):

        print(self.state)
