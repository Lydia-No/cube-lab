class Configuration:

    def __init__(self, data):
        self.data = list(data)

    def shift(self, k=1):
        n = len(self.data)
        k = k % n
        return Configuration(self.data[k:] + self.data[:k])

    def orbit(self, steps):

        states = []
        current = self

        for _ in range(steps):
            states.append(current)
            current = current.shift()

        return states

    def __repr__(self):
        return "".join(map(str, self.data))
