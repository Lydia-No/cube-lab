import numpy as np


class KCube:

    def __init__(self, dimension, k, initial_state=None):

        self.dimension = dimension
        self.k = k

        if initial_state is None:
            self.state = np.zeros(dimension, dtype=int)
        else:
            self.state = np.array(initial_state, dtype=int)

    def copy(self):

        return KCube(self.dimension, self.k, self.state.copy())

    def get_state(self):

        return tuple(int(x) for x in self.state)

    def increment_axis(self, axis):

        self.state[axis] = (self.state[axis] + 1) % self.k

    def decrement_axis(self, axis):

        self.state[axis] = (self.state[axis] - 1) % self.k

    def apply_vector(self, vector):

        for i, v in enumerate(vector):

            self.state[i] = (self.state[i] + v) % self.k

    def neighbors(self):

        neighbors = []

        for i in range(self.dimension):

            inc = self.copy()
            inc.increment_axis(i)
            neighbors.append(inc.get_state())

            dec = self.copy()
            dec.decrement_axis(i)
            neighbors.append(dec.get_state())

        return neighbors
