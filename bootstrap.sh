#!/usr/bin/env bash
set -euo pipefail

die() { echo "ERROR: $*" 1>&2; exit 1; }

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if git -C "$SCRIPT_DIR" rev-parse --show-toplevel >/dev/null 2>&1; then
  cd "$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
else
  cd "$SCRIPT_DIR"
fi

ensure_venv() {
  if [ ! -d ".venv" ]; then
    python3 -m venv .venv
  fi
  # shellcheck disable=SC1091
  source .venv/bin/activate
  python -m pip install -U pip wheel setuptools
}

init_submodules() {
  git submodule sync --recursive || true
  git submodule update --init --recursive
}

is_packaged_python_project() {
  local dir="$1"
  [ -f "$dir/pyproject.toml" ] || [ -f "$dir/setup.py" ]
}

add_to_venv_pth() {
  local dir="$1"
  python - <<PY
import site, pathlib
root = pathlib.Path("$dir").resolve()
paths = [root]
if (root / "src").is_dir():
    paths.append(root / "src")

pth_dir = pathlib.Path(site.getsitepackages()[0])
pth_file = pth_dir / "cube_lab_workspace.pth"

existing = []
if pth_file.exists():
    existing = [l.strip() for l in pth_file.read_text().splitlines() if l.strip()]

changed = False
for p in paths:
    s = str(p)
    if s not in existing:
        existing.append(s)
        changed = True
        print("Added to .pth:", s)

if changed:
    pth_file.write_text("\n".join(existing) + "\n")
else:
    print("No .pth changes")
PY
}

install_project() {
  local dir="$1"
  [ -d "$dir" ] || die "Missing directory: $dir (did submodules init?)"

  if is_packaged_python_project "$dir"; then
    pip install -e "$dir"
    return 0
  fi

  if [ -f "$dir/requirements.txt" ]; then
    pip install -r "$dir/requirements.txt"
  fi
  add_to_venv_pth "$dir"
}

resolve_hypercube_path() {
  if [ -d "hypercube-observer" ]; then echo "hypercube-observer"; return 0; fi
  if [ -d "cube-lab/hypercube-observer" ]; then echo "cube-lab/hypercube-observer"; return 0; fi
  return 1
}

run_tests() {
  python -m pip install -U pytest
  pytest -q
}

main() {
  ensure_venv
  init_submodules

  install_project symbolic-core
  install_project symbolic-dynamics-lab
  install_project symbolic-cube-explorer

  # symbolic-engine is a container; install its actual python subproject if present
  if [ -d "symbolic-engine/symbolic-dynamics-engine" ]; then
    install_project symbolic-engine/symbolic-dynamics-engine
  else
    install_project symbolic-engine
  fi

  hyper="$(resolve_hypercube_path)" || die "Missing hypercube-observer submodule"
  install_project "$hyper"

  run_tests
  echo "OK: workspace ready"
}

main "$@"
