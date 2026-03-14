.PHONY: init update test

init:
	@echo "Monorepo: no submodules."

update:
	git pull

test:
	python3 -m pytest -q
