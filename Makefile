.PHONY: init update test

init:
	git submodule update --init --recursive

update:
	git pull
	git submodule update --init --recursive

test:
	python -m pytest -q
