import random

from symbolic_dynamics.state_spaces.kcube import KCube
from symbolic_dynamics.walkers.symbolic_walker import SymbolicWalker
from symbolic_dynamics.observers.entropy import trajectory_entropy
from symbolic_dynamics.observers.attractor import detect_cycle


def run_cli():

    print("Symbolic Dynamics Lab CLI")
    print("Type sequences like: cave horse storm")
    print("Type 'quit' to exit\n")

    cube = KCube(3, 4)

    grammar = {
        "cave": (1, 0, 0),
        "horse": (0, 1, 0),
        "storm": (0, 0, 1),
        "ladder": (1, 1, 0)
    }

    walker = SymbolicWalker(cube, grammar)

    while True:

        seq = input("Enter symbolic sequence (or quit): ").strip()

        if seq == "quit":
            print("Exiting symbolic lab.")
            break

        if seq == "":
            continue

        sequence = seq.split()

        # Auto-create operators for new symbols
        for symbol in sequence:

            if symbol not in grammar:

                grammar[symbol] = (
                    random.choice([-1, 0, 1]),
                    random.choice([-1, 0, 1]),
                    random.choice([-1, 0, 1])
                )

                print(f"Created operator for new symbol: {symbol} -> {grammar[symbol]}")

        trajectory = walker.run(sequence)

        print("\nTrajectory:")
        for step in trajectory:
            print(step)

        entropy = trajectory_entropy(trajectory)
        print("\nEntropy:", entropy)

        cycle = detect_cycle(trajectory)

        if cycle:
            print("\nCycle detected:")
            print("Start index:", cycle["cycle_start"])
            print("Cycle length:", cycle["cycle_length"])
            print("Cycle states:", cycle["cycle_states"])
        else:
            print("\nNo cycle detected")

        print()
