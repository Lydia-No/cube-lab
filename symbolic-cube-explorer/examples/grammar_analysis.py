from cube_explorer.core import run_symbol_sequence
from cube_explorer.hypercube import Hypercube
from cube_explorer.analysis import (
    find_cycle,
    state_coverage,
    trajectory_entropy,
    transition_counts,
)

from cube_explorer.grammars.sefer import apply_sefer_symbol


cube = Hypercube(8)

import random

symbols = ["א","מ","ש"]
sequence = [random.choice(symbols) for _ in range(100)]

path = run_symbol_sequence(
    0,
    sequence,
    apply_sefer_symbol,
    cube,
)

print("Cube dimension:", cube.dimension)
print("Total states:", cube.states)
print()

print("Path length:", len(path))

coverage = state_coverage(path, cube.states)
print("State coverage:", coverage)

entropy = trajectory_entropy(path)
print("Trajectory entropy:", entropy)

cycle = find_cycle(path)
print("Cycle detected:", cycle)

print()

print("Transition counts:")
for k, v in transition_counts(path).items():
    print(k, v)
