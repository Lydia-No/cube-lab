from cube_explorer.hypercube import Hypercube


def run():

    dim = 3
    steps = 20

    cube = Hypercube(dim)

    seq = cube.random_walk(steps)

    print("\nSequence:", seq)


if __name__ == "__main__":
    run()
