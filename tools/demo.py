"""
Workspace demo runner.

- Prints what modules exist.
- Tries to run a tiny demo if likely entrypoints exist.
"""
from __future__ import annotations

import importlib
import inspect
from typing import Any


def maybe_import(name: str):
    try:
        return importlib.import_module(name)
    except Exception as e:
        return e


def find_callable(mod: Any, names: list[str]):
    for n in names:
        if hasattr(mod, n) and callable(getattr(mod, n)):
            return getattr(mod, n)
    return None


def main() -> None:
    modules = ["symbolic_core", "cube_explorer", "symbolic_dynamics", "hypercube_observer"]
    print("== imports ==")
    imported: dict[str, Any] = {}
    for m in modules:
        obj = maybe_import(m)
        imported[m] = obj
        if isinstance(obj, Exception):
            print(f"NO  {m}: {type(obj).__name__}: {obj}")
        else:
            print(f"OK  {m}: {getattr(obj, '__file__', '<namespace>')}")
    print()

    ce = imported.get("cube_explorer")
    if not isinstance(ce, Exception):
        print("== cube_explorer surface ==")
        public = [n for n in dir(ce) if not n.startswith("_")]
        print("count:", len(public))
        print("sample:", public[:30])
        print()

        # Try likely demo entrypoints without hardcoding one fragile function.
        candidates = [
            ("cube_explorer.core", ["run_symbol_sequence", "run", "main"]),
            ("cube_explorer", ["main"]),
        ]
        for mod_name, fn_names in candidates:
            mod = maybe_import(mod_name)
            if isinstance(mod, Exception):
                continue
            fn = find_callable(mod, fn_names)
            if fn is None:
                continue
            print(f"== running demo: {mod_name}.{fn.__name__} ==")
            try:
                sig = inspect.signature(fn)
                if len(sig.parameters) == 0:
                    fn()
                else:
                    print("Callable exists but needs args; skipping:", sig)
                return
            except Exception as e:
                print("Demo callable failed:", type(e).__name__, e)
                return

    print("No runnable demo entrypoint found automatically (still functional: imports/tests/install).")


if __name__ == "__main__":
    main()
