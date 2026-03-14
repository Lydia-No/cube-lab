import numpy as np
from .configuration import Configuration


class ShiftSpace:

    def __init__(self, alphabet):
        self.alphabet = alphabet

    def random_configuration(self, n):

        data = np.random.choice(self.alphabet, n)

        return Configuration(data)

    def shift(self, config, k=1):

        return config.shift(k)
