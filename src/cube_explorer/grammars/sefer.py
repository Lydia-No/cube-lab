from __future__ import annotations

from .base import GrammarMeta, MappingGrammar

# Mother letters as axes (minimal, deterministic, testable)
# א -> X (bit0), מ -> Y (bit1), ש -> Z (bit2)
SYMBOL_TO_AXIS = {"א": 0, "מ": 1, "ש": 2}

GRAMMAR = MappingGrammar(
    meta=GrammarMeta(
        name="sefer",
        display_name="Sefer (Hebrew Mothers → Axes)",
        description="Operational mapping: mother letters toggle cube axes (Q3).",
        version="0.1.0",
    ),
    symbol_to_axis=SYMBOL_TO_AXIS,
    dims=3,
)
