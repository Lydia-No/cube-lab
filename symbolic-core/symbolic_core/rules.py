from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable

from symbolic_core.state import SymbolicState


@dataclass(frozen=True, slots=True)
class LocalRule:
    """
    A simple local symbolic rule.

    If all bits in `condition_on` are 1 and all bits in `condition_off` are 0,
    then flip all bits in `flip_indices`.
    """
    condition_on: tuple[int, ...]
    condition_off: tuple[int, ...]
    flip_indices: tuple[int, ...]

    def applies(self, state: SymbolicState) -> bool:
        bits = state.bits
        return (
            all(bits[i] == 1 for i in self.condition_on)
            and all(bits[i] == 0 for i in self.condition_off)
        )

    def apply(self, state: SymbolicState) -> SymbolicState:
        if not self.applies(state):
            return state
        return state.flip_many(self.flip_indices)

    def signature(self) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
        return (self.condition_on, self.condition_off, self.flip_indices)


def generate_local_rules(
    n_bits: int,
    max_condition_size: int = 2,
    max_flip_size: int = 2,
) -> Iterable[LocalRule]:
    """
    Generate a manageable space of local rules.
    This is the beginning of the rule universe.
    """
    indices = tuple(range(n_bits))

    for cond_size in range(max_condition_size + 1):
        for on in combinations(indices, cond_size):
            remaining_after_on = [i for i in indices if i not in on]

            for off_size in range(max_condition_size + 1):
                for off in combinations(remaining_after_on, off_size):
                    for flip_size in range(1, max_flip_size + 1):
                        for flips in combinations(indices, flip_size):
                            yield LocalRule(
                                condition_on=tuple(sorted(on)),
                                condition_off=tuple(sorted(off)),
                                flip_indices=tuple(sorted(flips)),
                            )
