import argparse
from symbolic_dynamics.algorithms.pipeline import SFTPipeline


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--alphabet", default="01")
    parser.add_argument("--forbidden", default="000")

    args = parser.parse_args()

    alphabet = list(args.alphabet)

    forbidden = [args.forbidden]

    pipe = SFTPipeline(alphabet, forbidden)

    print("entropy:", pipe.entropy())


if __name__ == "__main__":
    main()
