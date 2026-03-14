from __future__ import annotations

import math
from collections import Counter

from symbolic_core.simulator import SimulationResult


def shannon_entropy(symbols: list[str]) -> float:
    if not symbols:
        return 0.0
    counts = Counter(symbols)
    total = len(symbols)
    return -sum((c / total) * math.log(c / total) for c in counts.values())


def score_simulation(result: SimulationResult) -> float:
    """
    Reward:
    - more unique states
    - some repetition (not dead, not pure freeze)
    - trajectory diversity

    Crude first-pass heuristic, but useful.
    """
    states_as_strings = [s.to_string() for s in result.trajectory]
    entropy = shannon_entropy(states_as_strings)

    score = 0.0
    score += result.unique_states * 1.5
    score += entropy * 3.0

    if result.first_repeat_step is not None:
        score += 5.0

    if len(set(states_as_strings)) == 1:
        score -= 10.0  # dead rule penalty

    return score
