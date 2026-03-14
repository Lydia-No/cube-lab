import random
from collections import defaultdict
from cube_explorer.hypercube import Hypercube


def vertex_to_point(vertex, dim):

    bits = format(vertex, f"0{dim}b")

    return tuple(1 if b == "1" else -1 for b in bits)


def run():

    dim = 4
    steps = 200

    cube = Hypercube(dim)

    vertex = random.randrange(1 << dim)

    seq = []
    vertices = [vertex]

    transitions = defaultdict(int)

    for _ in range(steps):

        candidates = []

        for d in range(dim):

            new_vertex = vertex ^ (1 << d)

            candidates.append((d,new_vertex))

        weights = []

        current_point = vertex_to_point(vertex,dim)

        for d,new_vertex in candidates:

            next_point = vertex_to_point(new_vertex,dim)

            w = transitions[(current_point,next_point)] + 1

            weights.append(w)

        choice = random.choices(candidates,weights=weights)[0]

        d,new_vertex = choice

        seq.append(cube.symbols[d])

        next_point = vertex_to_point(new_vertex,dim)

        transitions[(current_point,next_point)] += 1

        vertex = new_vertex

        vertices.append(vertex)

    print("\nGenerated sequence:\n")

    print(" ".join(seq[:50]))

    print("\nStrong transitions:\n")

    sorted_edges = sorted(transitions.items(),key=lambda x:-x[1])

    for (a,b),count in sorted_edges[:10]:

        print(a,"→",b," count=",count)


if __name__ == "__main__":
    run()
