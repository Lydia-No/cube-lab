import math
from collections import Counter


def trajectory_entropy(trajectory):

    counts = Counter(trajectory)

    total = len(trajectory)

    entropy = 0.0

    for count in counts.values():

        p = count / total

        entropy -= p * math.log2(p)

    return entropy
