from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence


DIM = 5

SYMBOL_TO_BIT = {
    "cave": 0,
    "horse": 1,
    "ladder": 2,
    "flowers": 3,
    "storm": 4,
}


def state_to_bits(state: int, dim: int = DIM) -> str:
    return format(state, f"0{dim}b")


def flip_dimension(state: int, bit: int) -> int:
    if bit < 0 or bit >= DIM:
        raise ValueError(f"Bit index out of range: {bit}")
    return state ^ (1 << bit)


def permute_axes(state: int, permutation: Sequence[int]) -> int:
    """
    Apply an axis permutation to a bitstate.

    permutation[new_pos] = old_pos

    Example:
        permutation = [1,2,3,4,0]
    means:
        new bit 0 gets old bit 1
        new bit 1 gets old bit 2
        ...
        new bit 4 gets old bit 0
    """
    if len(permutation) != DIM:
        raise ValueError(f"Permutation must have length {DIM}")

    if sorted(permutation) != list(range(DIM)):
        raise ValueError(f"Invalid permutation: {permutation}")

    new_state = 0
    for new_pos, old_pos in enumerate(permutation):
        bit_value = (state >> old_pos) & 1
        if bit_value:
            new_state |= (1 << new_pos)
    return new_state


@dataclass(frozen=True)
class HypercubeOperator:
    """
    A full hypercube symmetry action:
    - first permute axes
    - then apply flips on selected axes
    """
    name: str
    permutation: Sequence[int]
    flips: Sequence[int]

    def apply(self, state: int) -> int:
        new_state = permute_axes(state, self.permutation)
        for bit in self.flips:
            new_state = flip_dimension(new_state, bit)
        return new_state


IDENTITY_PERMUTATION = [0, 1, 2, 3, 4]

# Basic symbolic flips (your old Mimulus behavior)
BASIC_OPERATORS = {
    symbol: HypercubeOperator(
        name=symbol,
        permutation=IDENTITY_PERMUTATION,
        flips=[bit],
    )
    for symbol, bit in SYMBOL_TO_BIT.items()
}

# Some example symmetry operators
SYMMETRY_OPERATORS = {
    "rotate_forward": HypercubeOperator(
        name="rotate_forward",
        permutation=[1, 2, 3, 4, 0],
        flips=[],
    ),
    "rotate_backward": HypercubeOperator(
        name="rotate_backward",
        permutation=[4, 0, 1, 2, 3],
        flips=[],
    ),
    "swap_01": HypercubeOperator(
        name="swap_01",
        permutation=[1, 0, 2, 3, 4],
        flips=[],
    ),
    "swap_23": HypercubeOperator(
        name="swap_23",
        permutation=[0, 1, 3, 2, 4],
        flips=[],
    ),
}

# Combined operators: rotation + flip
COMBINED_OPERATORS = {
    "storm_twist": HypercubeOperator(
        name="storm_twist",
        permutation=[2, 0, 1, 4, 3],
        flips=[4],
    ),
    "flower_turn": HypercubeOperator(
        name="flower_turn",
        permutation=[0, 2, 1, 4, 3],
        flips=[3],
    ),
    "cave_shift": HypercubeOperator(
        name="cave_shift",
        permutation=[1, 0, 2, 4, 3],
        flips=[0],
    ),
}

ALL_OPERATORS = {}
ALL_OPERATORS.update(BASIC_OPERATORS)
ALL_OPERATORS.update(SYMMETRY_OPERATORS)
ALL_OPERATORS.update(COMBINED_OPERATORS)


def transform(state: int, symbol: str) -> int:
    """
    Backward-compatible interface.
    Applies either a basic symbol or a symmetry operator by name.
    """
    if symbol not in ALL_OPERATORS:
        raise ValueError(f"Unknown symbol/operator: {symbol}")
    return ALL_OPERATORS[symbol].apply(state)


def walk_sequence(start_state: int, sequence: Iterable[str]) -> List[int]:
    state = start_state
    path = [state]

    for symbol in sequence:
        state = transform(state, symbol)
        path.append(state)

    return path


def describe_walk(start_state: int, sequence: Iterable[str]) -> list[dict]:
    """
    Useful for debugging and visualization.
    Returns step-by-step state transitions.
    """
    state = start_state
    rows = [{
        "step": 0,
        "operator": "START",
        "state_int": state,
        "state_bits": state_to_bits(state),
    }]

    for i, symbol in enumerate(sequence, start=1):
        state = transform(state, symbol)
        rows.append({
            "step": i,
            "operator": symbol,
            "state_int": state,
            "state_bits": state_to_bits(state),
        })

    return rows


def available_operators() -> list[str]:
    return sorted(ALL_OPERATORS.keys())
