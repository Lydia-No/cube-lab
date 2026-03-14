#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

echo "== repo root =="
pwd
echo

echo "== submodules =="
git submodule status --recursive || true
echo

echo "== key dirs =="
for d in symbolic-core symbolic-dynamics-lab symbolic-cube-explorer symbolic-engine cube-lab/hypercube-observer hypercube-observer; do
  if [ -d "$d" ]; then
    echo "OK  $d"
  else
    echo "MISS $d"
  fi
done
echo

echo "== packaging check =="
for d in symbolic-core symbolic-dynamics-lab symbolic-cube-explorer symbolic-engine cube-lab/hypercube-observer hypercube-observer symbolic-engine/symbolic-dynamics-engine; do
  [ -d "$d" ] || continue
  if [ -f "$d/pyproject.toml" ] || [ -f "$d/setup.py" ]; then
    echo "PKG  $d"
  else
    echo "SRC  $d"
  fi
done
echo

if [ -d ".venv" ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
  echo "== python =="
  python -V
  echo
  echo "== import check =="
  python - <<'PY'
import importlib
mods = ["symbolic_core","cube_explorer","symbolic_dynamics","hypercube_observer"]
for m in mods:
    try:
        importlib.import_module(m)
        print("OK ", m)
    except Exception as e:
        print("NO ", m, "->", type(e).__name__, e)
PY
else
  echo "No .venv yet. Run: ./bootstrap.sh"
fi
