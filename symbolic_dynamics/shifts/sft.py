from symbolic_dynamics.core.shift_space import ShiftSpace


class SFT(ShiftSpace):

    def __init__(self, alphabet, forbidden):

        super().__init__(alphabet)

        self.forbidden = forbidden

    def admissible(self, sequence):

        s = "".join(sequence)

        for f in self.forbidden:
            if f in s:
                return False

        return True
