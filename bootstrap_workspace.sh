#!/usr/bin/env bash
set -e

echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing repositories..."

pip install -e symbolic-core
pip install -e symbolic-engine
pip install -e symbolic-dynamics-lab
pip install -e symbolic-cube-explorer
pip install -e hypercube-observer

echo "Installing dev tools..."
pip install pytest black ipython

echo "Creating integration tests..."

mkdir -p integration-tests

cat <<'PY' > integration-tests/test_engine_core.py
from symbolic_core.state import SymbolicState
from symbolic_core.rule import PermutationRule
from symbolic_core.engine import DynamicsEngine

def test_core_engine_step():
    s = SymbolicState(["A","B","C"])
    rule = PermutationRule(0,1)
    engine = DynamicsEngine([rule])
    new_state = engine.step(s)
    assert new_state.symbols == ("B","A","C")
PY

cat <<'PY' > integration-tests/test_pipeline.py
from symbolic_core.state import SymbolicState
from symbolic_core.rule import PermutationRule
from symbolic_core.engine import DynamicsEngine

def test_engine_pipeline():
    state = SymbolicState(["A","B","C","D"])
    rules = [
        PermutationRule(0,1),
        PermutationRule(2,3)
    ]
    engine = DynamicsEngine(rules)
    history = engine.run(state, 10)
    assert len(history) == 11
PY

cat <<'PY' > integration-tests/test_cube_explorer.py
import symbolic_cube_explorer

def test_cube_explorer_import():
    assert symbolic_cube_explorer is not None
PY

cat <<'PY' > integration-tests/test_hypercube_observer.py
import hypercube_observer

def test_hypercube_import():
    assert hypercube_observer is not None
PY

echo "Running tests..."
pytest integration-tests

echo "Workspace ready."
