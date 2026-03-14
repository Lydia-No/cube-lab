import argparse

from cube_explorer.hypercube import Hypercube
from cube_explorer.walkers.random_walk import RandomWalker
from cube_explorer.entropy.entropy import entropy
from cube_explorer.analysis.weights import weight_distribution, print_histogram


def cmd_run(args):
    cube = Hypercube(args.dim)
    walker = RandomWalker(cube)

    symbols = walker.symbols(args.steps)

    print("\nSymbolic sequence:\n")
    print(" ".join(symbols))


def cmd_entropy(args):
    cube = Hypercube(args.dim)
    walker = RandomWalker(cube)

    symbols = walker.symbols(args.steps)
    H = entropy(symbols)

    print(f"\nEntropy: {H:.6f}\n")


def cmd_weights(args):
    cube = Hypercube(args.dim)

    dist = weight_distribution(cube, args.steps)

    print_histogram(dist)


def main():
    parser = argparse.ArgumentParser(description="Symbolic Cube Explorer")
    sub = parser.add_subparsers(dest="command", required=True)

    run_cmd = sub.add_parser("run")
    run_cmd.add_argument("--dim", type=int, default=4)
    run_cmd.add_argument("--steps", type=int, default=50)
    run_cmd.set_defaults(func=cmd_run)

    entropy_cmd = sub.add_parser("entropy")
    entropy_cmd.add_argument("--dim", type=int, default=4)
    entropy_cmd.add_argument("--steps", type=int, default=10000)
    entropy_cmd.set_defaults(func=cmd_entropy)

    weights_cmd = sub.add_parser("weights")
    weights_cmd.add_argument("--dim", type=int, default=6)
    weights_cmd.add_argument("--steps", type=int, default=20000)
    weights_cmd.set_defaults(func=cmd_weights)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
