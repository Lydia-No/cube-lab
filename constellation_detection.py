from cube_explorer.hypercube import Hypercube
from collections import defaultdict


def vertex_to_point(vertex, dim):

    bits = format(vertex, f"0{dim}b")

    return tuple(1 if b == "1" else -1 for b in bits)


def detect_strong_edges(transitions, threshold=3):

    motifs = []

    for (a,b),count in transitions.items():

        if count >= threshold:

            motifs.append((a,b,count))

    motifs.sort(key=lambda x: -x[2])

    return motifs


def detect_cycles(sequence, length=4):

    cycles = defaultdict(int)

    for i in range(len(sequence)-length):

        c = tuple(sequence[i:i+length])

        cycles[c] += 1

    result = []

    for c,count in cycles.items():

        if count > 1:

            result.append((c,count))

    result.sort(key=lambda x:-x[1])

    return result


def run():

    dim = 4
    steps = 200

    cube = Hypercube(dim)

    seq,vertices = cube.random_walk(steps, return_vertices=True)

    transitions = defaultdict(int)

    prev = None

    for v in vertices:

        p = vertex_to_point(v,dim)

        if prev is not None:

            transitions[(prev,p)] += 1

        prev = p


    strong = detect_strong_edges(transitions)

    cycles = detect_cycles(seq)


    print("\nStrong transition motifs:\n")

    for a,b,c in strong[:10]:

        print(a,"→",b," count=",c)


    print("\nSymbolic cycles:\n")

    for c,count in cycles[:10]:

        print("".join(c)," count=",count)


if __name__ == "__main__":
    run()
