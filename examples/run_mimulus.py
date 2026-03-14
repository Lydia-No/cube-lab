from cube_explorer.grammars.mimulus import (
    walk_sequence,
    describe_walk,
    state_to_bits,
    available_operators,
)


def main() -> None:
    start_state = 0

    sequence = [
        "cave",
        "horse",
        "rotate_forward",
        "storm",
        "storm_twist",
        "flower_turn",
        "swap_01",
        "ladder",
    ]

    print("Available operators:")
    print(", ".join(available_operators()))
    print()

    print(f"Start state: {start_state} ({state_to_bits(start_state)})")
    print(f"Sequence: {sequence}")
    print()

    rows = describe_walk(start_state, sequence)
    for row in rows:
        print(
            f"step={row['step']:>2} "
            f"op={row['operator']:<15} "
            f"state={row['state_int']:>2} "
            f"bits={row['state_bits']}"
        )

    path = walk_sequence(start_state, sequence)
    print()
    print("Path:", path)


if __name__ == "__main__":
    main()
