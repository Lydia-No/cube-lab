# Hypercube Observer

Hypercube Observer is an experimental playground built on top of
Symbolic Cube Explorer.

It explores symbolic dynamics inside hypercube state spaces using:

• random walks
• entropy analysis
• attractor detection
• symbolic constellation visualization
• learning walkers

## Installation

Clone both repositories:

git clone https://github.com/Lydia-No/symbolic-cube-explorer.git
git clone https://github.com/Lydia-No/hypercube-observer.git

Create environment:

python3 -m venv .venv
source .venv/bin/activate

Install engine:

pip install -e ../symbolic-cube-explorer

Install dependencies:

pip install plotly networkx

## Example

Run cube walk visualization:

python cube_cli.py cube
