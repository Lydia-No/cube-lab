from __future__ import annotations

from .base import GrammarMeta, MappingGrammar

# Minimal runnable rune mapping (3 symbols → 3 axes).
# You can remap later; the point is that the plugin exists and is executable.
# ᚠ (Fehu) -> X, ᚢ (Uruz) -> Y, ᚦ (Thurisaz) -> Z
SYMBOL_TO_AXIS = {"ᚠ": 0, "ᚢ": 1, "ᚦ": 2}

GRAMMAR = MappingGrammar(
    meta=GrammarMeta(
        name="runes",
        display_name="Runes (3 Runes → Axes)",
        description="Operational mapping: three runes toggle cube axes (Q3).",
        version="0.1.0",
    ),
    symbol_to_axis=SYMBOL_TO_AXIS,
    dims=3,
)
