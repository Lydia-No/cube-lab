from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SymbolicState:
    """
    Minimal immutable symbolic state.

    For the first version, we model a state as a bitstring.
    This is simple, hashable, and fast enough to support large rule search.
    """
    bits: tuple[int, ...]

    @classmethod
    def from_string(cls, s: str) -> "SymbolicState":
        return cls(tuple(int(ch) for ch in s))

    def to_string(self) -> str:
        return "".join(str(b) for b in self.bits)

    def flip(self, index: int) -> "SymbolicState":
        if index < 0 or index >= len(self.bits):
            raise IndexError(f"Index out of range: {index}")
        new_bits = list(self.bits)
        new_bits[index] = 1 - new_bits[index]
        return SymbolicState(tuple(new_bits))

    def flip_many(self, indices: tuple[int, ...]) -> "SymbolicState":
        new_bits = list(self.bits)
        for i in indices:
            if i < 0 or i >= len(new_bits):
                raise IndexError(f"Index out of range: {i}")
            new_bits[i] = 1 - new_bits[i]
        return SymbolicState(tuple(new_bits))

    def __len__(self) -> int:
        return len(self.bits)
