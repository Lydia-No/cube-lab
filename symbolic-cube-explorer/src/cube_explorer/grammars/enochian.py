from __future__ import annotations

from .base import GrammarMeta, MappingGrammar

# Minimal runnable Enochian-like mapping.
# Note: There is no Unicode-standard “Enochian script”; we use Latin tokens.
# You can swap these tokens to whatever your project uses.
SYMBOL_TO_AXIS = {"OL": 0, "PA": 1, "NA": 2}

GRAMMAR = MappingGrammar(
    meta=GrammarMeta(
        name="enochian",
        display_name="Enochian (3 Tokens → Axes)",
        description="Operational mapping: three Enochian tokens toggle cube axes (Q3).",
        version="0.1.0",
    ),
    symbol_to_axis=SYMBOL_TO_AXIS,
    dims=3,
)
