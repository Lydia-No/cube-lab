from collections import defaultdict


def transition_matrix(seq):

    counts = defaultdict(lambda: defaultdict(int))

    for i in range(len(seq) - 1):

        a = seq[i]
        b = seq[i + 1]

        counts[a][b] += 1

    matrix = {}

    for a in counts:

        total = sum(counts[a].values())

        matrix[a] = {}

        for b in counts[a]:

            matrix[a][b] = counts[a][b] / total

    return matrix


def print_matrix(matrix):

    symbols = sorted(matrix.keys())

    print("\nTransition matrix\n")

    header = "    " + " ".join(symbols)
    print(header)

    for a in symbols:

        row = [f"{matrix[a].get(b,0):.2f}" for b in symbols]

        print(f"{a} | " + " ".join(row))
