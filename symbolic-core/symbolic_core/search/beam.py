from __future__ import annotations

from dataclasses import dataclass

from symbolic_core.rules import LocalRule, generate_local_rules
from symbolic_core.scoring import score_simulation
from symbolic_core.simulator import run_rule
from symbolic_core.state import SymbolicState


@dataclass(slots=True)
class RuleCandidate:
    rule: LocalRule
    score: float
    unique_states: int
    first_repeat_step: int | None


def search_rules(
    initial: SymbolicState,
    n_bits: int,
    steps: int = 32,
    max_condition_size: int = 2,
    max_flip_size: int = 2,
    top_k: int = 20,
) -> list[RuleCandidate]:
    candidates: list[RuleCandidate] = []

    for rule in generate_local_rules(
        n_bits=n_bits,
        max_condition_size=max_condition_size,
        max_flip_size=max_flip_size,
    ):
        result = run_rule(initial=initial, rule=rule, steps=steps)
        score = score_simulation(result)

        candidates.append(
            RuleCandidate(
                rule=rule,
                score=score,
                unique_states=result.unique_states,
                first_repeat_step=result.first_repeat_step,
            )
        )

    candidates.sort(key=lambda c: c.score, reverse=True)
    return candidates[:top_k]
