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

echo "=== Creating virtual environment ==="
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate

echo "=== Upgrading pip ==="
python -m pip install -U pip wheel setuptools

echo "=== Installing repos (editable) ==="
pip install -e symbolic-core
pip install -e symbolic-engine
pip install -e symbolic-dynamics-lab
pip install -e symbolic-cube-explorer

HYPER="$(resolve_hypercube_path)" || { echo "Missing hypercube-observer submodule"; exit 1; }
pip install -e "$HYPER"

echo "=== Installing dev tools ==="
pip install -U pytest black ipython

echo "=== Running tests ==="
pytest -q

echo "=== Workspace ready ==="
