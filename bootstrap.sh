#!/usr/bin/env bash
set -euo pipefail

die() {
  echo "ERROR: $*" 1>&2
  exit 1
}

ensure_https_submodules() {
  if [ ! -f ".gitmodules" ]; then
    return 0
  fi
  if grep -qE 'git@github\.com:' .gitmodules; then
    perl -pi -e 's#git\@github\.com:([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)(?:\.git)?#https://github.com/$1.git#g' .gitmodules
    git submodule sync --recursive
  fi
}

init_submodules() {
  git submodule update --init --recursive
}

ensure_venv() {
  if [ ! -d ".venv" ]; then
    python3 -m venv .venv
  fi
  # shellcheck disable=SC1091
  source .venv/bin/activate
  python -m pip install -U pip wheel setuptools
}

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

editable_installs() {
  pip install -e symbolic-core
  pip install -e symbolic-dynamics-lab
  pip install -e symbolic-cube-explorer
  pip install -e symbolic-engine

  local hyper
  hyper="$(resolve_hypercube_path)" || die "hypercube-observer submodule not found. Run: git submodule update --init --recursive"
  pip install -e "$hyper"
}

run_tests() {
  if command -v pytest >/dev/null 2>&1; then
    pytest -q
  else
    python -m pytest -q
  fi
}

main() {
  ensure_https_submodules
  init_submodules
  ensure_venv
  editable_installs
  run_tests
  echo "OK: workspace ready"
}

main "$@"
