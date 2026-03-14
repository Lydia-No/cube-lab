.PHONY: init update test

init:
	@echo "Monorepo: no submodules to init."

update:
	git pull

test:
	python -m pytest -q
