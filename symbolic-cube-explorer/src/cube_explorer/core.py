from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import List, Sequence, Tuple

from .grammars.base import BaseGrammar
from .utils import score_sequence


@dataclass(frozen=True)
class CubeGraph:
    """
    Q3 hypercube on vertices 0..7.
    Neighbor along axis k is v ^ (1 << k).
    """
    dims: int = 3

    def neighbors(self, v: int) -> List[int]:
        return [v ^ (1 << k) for k in range(self.dims)]


def concept_seed(concept: str, *, dims: int = 3) -> int:
    h = hashlib.sha256(concept.encode("utf-8")).digest()
    return h[0] % (1 << dims)


def execute_sequence(
    *,
    start: int,
    symbols: Sequence[str],
    grammar: BaseGrammar,
) -> Tuple[List[int], List[str], int]:
    """
    Core state engine:
      - validates with grammar
      - applies symbol-to-state transitions
      - returns (path, symbols, score)

    This is independent of which grammar you're using.
    """
    grammar.validate_sequence(symbols)

    state = start
    path: List[int] = [state]
    for s in symbols:
        state = grammar.apply_symbol(state, s)
        path.append(state)

    score = score_sequence(list(symbols))
    return path, list(symbols), score


@dataclass
class SymbolicWalker:
    """
    Convenience wrapper around CubeGraph + grammar.
    Keeps API close to your existing code, but defers meaning to grammar plugins.
    """
    cube: CubeGraph
    grammar: BaseGrammar

    def run_concept(self, concept: str, *, symbols: Sequence[str]) -> Tuple[int, List[int], List[str], int]:
        start = concept_seed(concept, dims=self.cube.dims)
        path, seq, score = execute_sequence(start=start, symbols=symbols, grammar=self.grammar)
        return start, path, seq, score
