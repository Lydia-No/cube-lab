from symbolic_dynamics.core.examples import (
    golden_mean_shift,
    even_shift,
    no_three_consecutive_ones
)


systems = [
    golden_mean_shift(),
    even_shift(),
    no_three_consecutive_ones()
]


for s in systems:

    print("Alphabet:", s.alphabet)
    print("Forbidden:", s.forbidden)

    print("Words length 5:")
    print(s.words(5))

    print("Entropy estimate:")
    print(s.entropy_estimate())

    print()
