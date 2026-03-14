init:
	git submodule update --init --recursive

update:
	git pull
	git submodule update --init --recursive

venv:
	python3 -m venv .venv
	. .venv/bin/activate && python -m pip install -U pip wheel setuptools

bootstrap:
	./bootstrap.sh

test:
	pytest -q
