SHELL := /bin/bash
PY := python

.PHONY: help venv deps cube network sky tesseract interior signature cluster metrics synth clean

help:
	@echo "Targets:"
	@echo "  make deps            Install python deps (plotly/numpy/kaleido)"
	@echo "  make cube            Run cube demo"
	@echo "  make network         Run network demo"
	@echo "  make sky             Run observer sky demo"
	@echo "  make interior        Run interior observer view (sky edges)"
	@echo "  make signature        Print signature JSON"
	@echo "  make cluster          Cluster many runs"
	@echo "  make metrics          Print windowed metrics"
	@echo "  make synth            Synthesize square motif + render HTML"
	@echo "  make clean           Remove generated html/png/json artifacts"

deps:
	$(PY) -m pip install -U pip
	$(PY) -m pip install -U numpy plotly kaleido

cube:
	$(PY) cube_cli.py cube

network:
	$(PY) cube_cli.py network

sky:
	$(PY) cube_cli.py sky

tesseract:
	$(PY) cube_cli.py tesseract

interior:
	$(PY) cube_cli.py interior --dim 3 --steps 2000 --observer-view --edge-view sky --save-html sky.html

signature:
	$(PY) cube_cli.py signature --dim 3 --steps 3000 --seed 7 --slow-min-weight 3

cluster:
	$(PY) cube_cli.py cluster --n 80 --dim 3 --steps 2500 --seed0 1 --slow-min-weight 3

metrics:
	$(PY) cube_cli.py metrics --dim 3 --steps 5000 --window 200

synth:
	$(PY) synth_demo.py --dim 3 --motif square --steps 700 --restarts 12 --iters 500 \
		--out-actions best_actions.json \
		--render-html synth_square.html --observer-view --edge-view sky

clean:
	rm -f *.html *.png best_actions.json *_actions.json
