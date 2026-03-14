from collections import defaultdict


def find_symbol_cycles(sequence, min_length=2, max_length=10):
    """
    Detect repeating symbolic cycles in a sequence.
    """

    cycles = defaultdict(int)
    n = len(sequence)

    for L in range(min_length, max_length + 1):

        for i in range(n - L):

            window = tuple(sequence[i:i + L])

            for j in range(i + L, n - L):

                if sequence[j:j + L] == list(window):
                    cycles[window] += 1
                    break

    results = []

    for cycle, count in cycles.items():
        results.append({
            "cycle": "".join(cycle),
            "length": len(cycle),
            "occurrences": count
        })

    results.sort(key=lambda x: -x["occurrences"])

    return results
