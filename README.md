# cube-lab

`cube-lab` is a **hub repository** for the Cube Lab workspace. It pins a compatible set of component repositories via **Git submodules**, and provides scripts + integration tests to bootstrap and validate the environment.

## What’s in here

- **Submodules**: component codebases (version-pinned by commit)
- **Workspace scripts**: bootstrap/setup/dev helpers
- **Integration tests**: quick checks for imports and pipeline wiring
- **Makefile**: convenience targets

## Included repositories (submodules)

| Path | Repo |
|---|---|
| `symbolic-core/` | `git@github.com:Lydia-No/symbolic-core.git` |
| `symbolic-cube-explorer/` | `git@github.com:Lydia-No/symbolic-cube-explorer.git` |
| `symbolic-dynamics-lab/` | `git@github.com:Lydia-No/symbolic-dynamics-lab.git` |
| `cube-lab/hypercube-observer/` | `git@github.com:Lydia-No/hypercube-observer.git` |
| `symbolic-engine/symbolic-dynamics-engine/` | `git@github.com:Lydia-No/symbolic-dynamics-engine.git` |

## Quick start

### Clone + init submodules

```bash
git clone git@github.com:Lydia-No/cube-lab.git
cd cube-lab
git submodule update --init --recursive
./bootstrap_workspace.sh
