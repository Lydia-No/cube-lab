import math
from collections import Counter


def entropy(sequence):
    """
    Compute Shannon entropy of a symbolic sequence.
    """

    counts = Counter(sequence)

    n = len(sequence)

    H = 0.0

    for c in counts.values():
        p = c / n
        H -= p * math.log2(p)

    return H
