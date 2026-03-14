import importlib
import pkgutil
from types import ModuleType

import pytest


CANDIDATES = [
    "symbolic_core",
    "cube_explorer",
    "symbolic_dynamics",
]


def try_import(name: str) -> ModuleType | None:
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError:
        return None


@pytest.mark.parametrize("module_name", CANDIDATES)
def test_import_known_candidates(module_name: str) -> None:
    mod = try_import(module_name)
    assert mod is not None, f"Expected importable module '{module_name}' (check .pth and installs)"


def test_discover_cube_explorer_symbols() -> None:
    mod = try_import("cube_explorer")
    if mod is None:
        pytest.skip("cube_explorer not importable")
    names = sorted([m.name for m in pkgutil.iter_modules(mod.__path__)])  # type: ignore[attr-defined]
    assert names, "cube_explorer imported but has no submodules"
