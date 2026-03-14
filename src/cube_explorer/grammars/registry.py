from __future__ import annotations

import importlib
import pkgutil
from typing import Dict, List

from .base import BaseGrammar

_PACKAGE = __name__.rsplit(".", 1)[0]  # cube_explorer.grammars


def _iter_modules() -> List[str]:
    pkg = importlib.import_module(_PACKAGE)
    out: List[str] = []
    for m in pkgutil.iter_modules(pkg.__path__):  # type: ignore[attr-defined]
        if m.name in {"base", "registry"}:
            continue
        out.append(m.name)
    return sorted(out)


def list_grammars() -> List[str]:
    return _iter_modules()


def get_grammar(name: str) -> BaseGrammar:
    mod = importlib.import_module(f"{_PACKAGE}.{name}")
    grammar = getattr(mod, "GRAMMAR", None)
    if grammar is None:
        raise KeyError(f"Grammar module '{name}' has no GRAMMAR object")
    # runtime structural check (Protocol)
    if not isinstance(grammar, BaseGrammar):  # type: ignore[arg-type]
        # Protocol runtime check is shallow; keep error explicit.
        missing = [m for m in ("symbols", "apply_symbol", "validate_sequence", "metadata") if not hasattr(grammar, m)]
        raise TypeError(f"Grammar '{name}' does not satisfy BaseGrammar. Missing: {missing}")
    return grammar
