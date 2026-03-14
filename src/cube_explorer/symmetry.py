from collections import Counter


def symbol_frequencies(sequence):
    """
    Count frequency of each symbol.
    """
    return Counter(sequence)


def symmetry_score(sequence):
    """
    Measure how uniform symbol frequencies are.
    Perfect symmetry -> all symbols appear equally.
    """

    counts = symbol_frequencies(sequence)

    if not counts:
        return 0

    values = list(counts.values())

    mean = sum(values) / len(values)

    deviation = sum(abs(v - mean) for v in values) / len(values)

    score = 1 / (1 + deviation)

    return score, counts
