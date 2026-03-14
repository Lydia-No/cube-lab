# Symbolic Cube Explorer

Symbolic Cube Explorer is a computational playground for exploring **symbolic dynamics on hypercube graphs (Qₙ)**.

Random walks on hypercubes generate symbolic sequences.
This project analyzes those sequences using entropy, attractor detection, and graph visualization.

The goal is to turn hypercube traversal into a **computational laboratory for symbolic systems**.

---

# Features

## Hypercube Engine

Supports hypercubes from **Q3 → Q8**.

| Dimension | Vertices | Edges |
| --------- | -------- | ----- |
| Q3        | 8        | 12    |
| Q4        | 16       | 32    |
| Q5        | 32       | 80    |
| Q6        | 64       | 192   |
| Q7        | 128      | 448   |
| Q8        | 256      | 1024  |

Each edge corresponds to flipping a single bit.

---

# Symbolic Dynamics

Each dimension flip emits a symbol.

Example mapping:

dimension 0 → A
dimension 1 → B
dimension 2 → C
dimension 3 → D

Example sequence:

A B C A D C B A ...

This transforms hypercube traversal into a **symbolic dynamical system**.

---

# Experiments

## Entropy Analysis

Measure entropy of symbolic sequences.

Run:

python examples/entropy_heatmap.py

Example output:

Q3 entropy: 1.58
Q4 entropy: 2.00
Q5 entropy: 2.32
Q6 entropy: 2.58

---

## Attractor Detection

Detect repeating symbolic cycles.

Run:

python examples/attractor_scan.py

Example output:

ABAC (len=4)
BCDA (len=4)
ACBD (len=4)

These motifs reveal **attractor structures** in hypercube walks.

---

# Visualization

## Cube Visualization

python examples/visualize_cube.py

Displays an **interactive 3D cube**.

---

## Tesseract Visualization

python examples/visualize_q4_tesseract.py

Shows a **projection of a 4D hypercube (tesseract)**.

---

## Animated Hypercube Walker

python examples/animate_cube_walk.py

Displays a walker moving through the cube.

---

## Symbol Transition Graph

python examples/symbol_transition_graph.py

Visualizes symbolic transitions such as:

A → B → C
↑       ↓
D ← E ← F

---

# Installation

Clone the repository:

git clone https://github.com/Lydia-No/symbolic-cube-explorer.git
cd symbolic-cube-explorer

Create environment:

python3 -m venv .venv
source .venv/bin/activate

Install dependencies:

pip install -e .
pip install plotly networkx

---

# Project Structure

src/cube_explorer/

* hypercube.py
* analysis.py
* attractors.py
* grammars/

examples/

* visualize_cube.py
* visualize_q4_tesseract.py
* animate_cube_walk.py
* entropy_heatmap.py
* symbol_transition_graph.py

---

# Research Directions

Possible research topics:

* symbolic dynamics on hypercube graphs
* entropy growth in higher dimensions
* attractor motifs
* symbolic grammar emergence
* hypercube symmetry groups

---

# License

MIT License
