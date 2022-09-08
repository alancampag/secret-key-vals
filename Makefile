SRCDIR = secretkv
VENV = .venv

.PHONY: develop install format lint test clean

develop:
	python3 -m venv $(VENV)
	. $(VENV)/bin/activate; \
	pip install wheel; \
	pip install -e .[dev]; \

install:
	python3 -m venv $(VENV)
	. $(VENV)/bin/activate; \
	pip install wheel; \
	pip install .[dev]; \

format: 
	black $(SRCDIR)

lint: 
	mypy $(SRCDIR)
	flake8 $(SRCDIR)

test:
	pytest -vs --cov
	coverage html

clean:
	rm -rf $(VENV)
	rm -rf *.egg-info
	rm -rf .mypy_cache
	rm -rf .vscode
	rm -rf htmlcov
