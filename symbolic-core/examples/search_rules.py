from symbolic_core.search.beam import search_rules
from symbolic_core.state import SymbolicState


def main() -> None:
    initial = SymbolicState.from_string("0101")

    top = search_rules(
        initial=initial,
        n_bits=4,
        steps=24,
        max_condition_size=2,
        max_flip_size=2,
        top_k=10,
    )

    for i, candidate in enumerate(top, start=1):
        print(f"\n#{i}")
        print(f"score={candidate.score:.3f}")
        print(f"unique_states={candidate.unique_states}")
        print(f"first_repeat_step={candidate.first_repeat_step}")
        print(f"rule={candidate.rule.signature()}")


if __name__ == "__main__":
    main()
