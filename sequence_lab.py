import argparse
from collections import defaultdict
import math

def entropy(sequence):

    from collections import Counter
    import math

    counts = Counter(sequence)

    total = len(sequence)

    H = 0

    for c in counts.values():

        p = c / total

        H -= p * math.log2(p)

    return H

from cube_explorer.hypercube import Hypercube
from cube_explorer.attractors import find_symbol_cycles


def sequence_to_walk(sequence, dim):

    cube = Hypercube(dim)

    symbol_map = {cube.symbols[i]: i for i in range(dim)}

    vertex = 0

    vertices = [vertex]

    transitions = defaultdict(int)

    for s in sequence:

        if s not in symbol_map:
            continue

        d = symbol_map[s]

        new_vertex = vertex ^ (1 << d)

        transitions[(vertex, new_vertex)] += 1

        vertex = new_vertex

        vertices.append(vertex)

    return vertices, transitions


def transition_report(transitions):

    ranked = sorted(transitions.items(), key=lambda x: -x[1])

    print("\nStrongest transitions:\n")

    for (a, b), count in ranked[:10]:

        print(f"{a} -> {b}   count={count}")


def run(sequence, dim):

    print("\nSequence length:", len(sequence))

    H = entropy(sequence)

    print("Entropy:", round(H, 4))

    vertices, transitions = sequence_to_walk(sequence, dim)

    transition_report(transitions)

    cycles = find_symbol_cycles(sequence)

    print("\nSymbolic motifs:\n")

    for c in cycles[:10]:

        print(f"{c['cycle']}  len={c['length']}  count={c['occurrences']}")


def main():

    parser = argparse.ArgumentParser(
        description="Hypercube sequence analysis"
    )

    parser.add_argument(
        "--seq",
        type=str,
        help="sequence string"
    )

    parser.add_argument(
        "--file",
        type=str,
        help="file containing sequence"
    )

    parser.add_argument(
        "--dim",
        type=int,
        default=4
    )

    args = parser.parse_args()

    if args.seq:

        sequence = args.seq.strip().upper()

    elif args.file:

        with open(args.file) as f:

            sequence = f.read().strip().upper()

    else:

        print("Provide --seq or --file")

        return

    run(sequence, args.dim)


if __name__ == "__main__":
    main()
