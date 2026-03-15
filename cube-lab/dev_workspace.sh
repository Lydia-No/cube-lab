#!/usr/bin/env bash
set -euo pipefail

resolve_hypercube_path() {
  if [ -d "hypercube-observer" ]; then
    echo "hypercube-observer"
    return 0
  fi
  if [ -d "cube-lab/hypercube-observer" ]; then
    echo "cube-lab/hypercube-observer"
    return 0
  fi
  return 1
}

echo "=== Activating environment ==="
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

echo "=== Upgrading pip ==="
python -m pip install -U pip wheel setuptools

echo "=== Installing repositories ==="
pip install -e symbolic-core
pip install -e symbolic-engine
pip install -e symbolic-dynamics-lab
pip install -e symbolic-cube-explorer

HYPER="$(resolve_hypercube_path)" || { echo "Missing hypercube-observer submodule"; exit 1; }
pip install -e "$HYPER"

echo "=== Installing development tools ==="
pip install -U pytest black ipython networkx matplotlib

echo "=== Creating state graph explorer ==="
mkdir -p tools
cat <<'PY' > tools/state_graph_explorer.py
import matplotlib.pyplot as plt
import networkx as nx

from symbolic_core.engine import DynamicsEngine
from symbolic_core.rule import PermutationRule
from symbolic_core.state import SymbolicState


def generate_graph(depth: int = 5) -> nx.DiGraph:
    start = SymbolicState(["A", "B", "C", "D"])
    rules = [
        PermutationRule(0, 1),
        PermutationRule(1, 2),
        PermutationRule(2, 3),
    ]
    engine = DynamicsEngine(rules)
    g = nx.DiGraph()
    current = start
    for _ in range(depth):
        next_state = engine.step(current)
        g.add_node(str(current))
        g.add_node(str(next_state))
        g.add_edge(str(current), str(next_state))
        current = next_state
    return g


def visualize() -> None:
    g = generate_graph()
    pos = nx.spring_layout(g)
    nx.draw(g, pos, with_labels=True)
    plt.show()


if __name__ == "__main__":
    visualize()
PY

echo "=== Done ==="
echo "Run: python tools/state_graph_explorer.py"
