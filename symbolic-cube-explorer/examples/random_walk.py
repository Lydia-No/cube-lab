#!/usr/bin/env python3
from cube_explorer.hypercube import Hypercube


def main():

    cube = Hypercube(4)

    seq = cube.random_walk(50)

    print("Random walk symbolic sequence:\n")

    print(" ".join(seq))


if __name__ == "__main__":
    main()
