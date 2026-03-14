import math
from collections import Counter


def entropy(seq):
    counts = Counter(seq)
    total = len(seq)

    if total == 0:
        return 0.0

    H = 0.0

    for c in counts.values():
        p = c / total
        H -= p * math.log2(p)

    return H
