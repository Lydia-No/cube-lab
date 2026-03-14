import itertools
import numpy as np


def build_sft_matrix(alphabet, forbidden, k=2):

    states = [''.join(p) for p in itertools.product(alphabet, repeat=k-1)]

    index = {s: i for i, s in enumerate(states)}

    A = np.zeros((len(states), len(states)))

    for s in states:

        for a in alphabet:

            new_word = s + a

            if any(f in new_word for f in forbidden):
                continue

            next_state = new_word[1:]

            i = index[s]
            j = index[next_state]

            A[i][j] = 1

    return A, states
