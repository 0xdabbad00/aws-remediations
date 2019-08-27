.DEFAULT_GOAL := ci  # The default target if you just run "make"

venv-setup: # Setup Python venv
	rm -rf venv/
	python3 -m venv venv

install: # Install dependencies in Python venv
	. venv/bin/activate
	pip3 install --user -r requirements.txt

setup: venv-setup install

fmt:  # Format Python source
	yapf --in-place --parallel --recursive src

lint:  # Format, style, and type linting
	yapf --diff --parallel --recursive src
	bandit -r src
	pylint src
	mypy src --disallow-untyped-defs --ignore-missing-imports --warn-unused-ignores

test: # Run unit tests
	nose2 --with-coverage --coverage src --coverage-config setup.cfg

ci: fmt lint test
