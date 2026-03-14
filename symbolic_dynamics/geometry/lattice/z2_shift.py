import numpy as np


class Z2Shift:

    def __init__(self, alphabet, size):

        self.alphabet = alphabet
        self.size = size

        self.state = np.random.choice(alphabet, (size, size))

    def shift_x(self):

        self.state = np.roll(self.state, 1, axis=0)

    def shift_y(self):

        self.state = np.roll(self.state, 1, axis=1)

    def show(self):

        print(self.state)
