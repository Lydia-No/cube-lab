from collections import Counter
from tqdm import tqdm


def vertex_weight(vertex):
    return sum(int(x) for x in vertex)


def weight_distribution(cube, steps):
    vertex = cube.random_vertex()
    weights = [vertex_weight(vertex)]

    for _ in tqdm(range(steps), desc="Walking cube", unit="step"):
        vertex, _ = cube.step(vertex)
        weights.append(vertex_weight(vertex))

    return Counter(weights)


def print_histogram(dist):
    print("\nWeight distribution\n")

    max_count = max(dist.values())
    scale = max(1, max_count // 40)

    for w in sorted(dist):
        bar = "█" * (dist[w] // scale)
        print(f"{w:2d} {bar}")
