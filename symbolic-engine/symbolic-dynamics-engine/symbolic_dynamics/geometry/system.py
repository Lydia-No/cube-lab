class SymbolicSystem:

    def __init__(self, dimension, alphabet):

        self.dimension = dimension
        self.alphabet = alphabet

    def info(self):

        print("dimension:", self.dimension)
        print("alphabet:", self.alphabet)
