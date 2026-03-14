from __future__ import annotations

from dataclasses import dataclass

from symbolic_core.rules import LocalRule
from symbolic_core.state import SymbolicState


@dataclass(slots=True)
class SimulationResult:
    trajectory: list[SymbolicState]
    unique_states: int
    first_repeat_step: int | None


def run_rule(
    initial: SymbolicState,
    rule: LocalRule,
    steps: int = 32,
) -> SimulationResult:
    """
    Deterministic evolution under one rule.
    """
    seen: dict[SymbolicState, int] = {}
    trajectory: list[SymbolicState] = [initial]
    seen[initial] = 0
    current = initial
    first_repeat_step: int | None = None

    for step in range(1, steps + 1):
        current = rule.apply(current)
        trajectory.append(current)

        if current in seen and first_repeat_step is None:
            first_repeat_step = step
        else:
            seen[current] = step

    return SimulationResult(
        trajectory=trajectory,
        unique_states=len(set(trajectory)),
        first_repeat_step=first_repeat_step,
    )
