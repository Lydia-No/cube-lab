from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Protocol, Sequence, runtime_checkable


@dataclass(frozen=True)
class GrammarMeta:
    name: str
    display_name: str
    description: str = ""
    version: str = "0.1.0"
    axes: int = 3


@runtime_checkable
class BaseGrammar(Protocol):
    """
    Grammar plugin contract.

    Must:
      - symbols(): iterable of accepted symbols
      - apply_symbol(state, symbol): returns next_state
      - validate_sequence(sequence): raises ValueError if invalid
      - metadata(): GrammarMeta

    Optional:
      - symbol_to_axis mapping for introspection
    """

    def symbols(self) -> Iterable[str]: ...
    def apply_symbol(self, state: int, symbol: str) -> int: ...
    def validate_sequence(self, sequence: Sequence[str]) -> None: ...
    def metadata(self) -> GrammarMeta: ...


class MappingGrammar:
    """
    Simple implementation helper: map symbol -> axis (0..dims-1), then toggle that bit.

    Works for Q3/Qn where "move along axis k" is state ^ (1<<k).
    """
    def __init__(
        self,
        *,
        meta: GrammarMeta,
        symbol_to_axis: Mapping[str, int],
        dims: int = 3,
    ) -> None:
        self._meta = meta
        self._symbol_to_axis: Dict[str, int] = dict(symbol_to_axis)
        self._dims = dims

    @property
    def symbol_to_axis(self) -> Dict[str, int]:
        return dict(self._symbol_to_axis)

    def symbols(self) -> List[str]:
        return list(self._symbol_to_axis.keys())

    def validate_sequence(self, sequence: Sequence[str]) -> None:
        bad = [s for s in sequence if s not in self._symbol_to_axis]
        if bad:
            known = sorted(self._symbol_to_axis.keys())
        raise ValueError(
            f"Invalid symbols for {self._meta.name}: {sorted(set(bad))}. "
            f"Known({len(known)}): {known}"
        )

    def apply_symbol(self, state: int, symbol: str) -> int:
        axis = self._symbol_to_axis[symbol]
        if axis < 0 or axis >= self._dims:
            raise ValueError(f"Axis out of range: {axis} for dims={self._dims}")
        return state ^ (1 << axis)

    def metadata(self) -> GrammarMeta:
        return self._meta
