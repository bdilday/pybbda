.PHONY: lint \
test-analysis test-data test-markov test \
clean \
install-dev install \
dist

lint: install-dev
	python -m black pybbda/ tests/ examples/
	python -m flake8 pybbda
	python -m flake8 tests
	python -m flake8 examples


test-analysis: install-dev
	python -m pytest tests/analysis/

test-data: install-dev
	python -m pytest tests/data/

test-markov: install
	python -m pybbda.analysis.run_expectancy.markov.cli \
	-b 0 0.1 0.1 0.1 0.1 0.1 \
	-i 1 henderi01_1982

test: install-dev
	python -m pytest tests/

clean-docs:
	cd docs && make clean
	rm -fr docs/auto_examples

clean-data:
	rm -rf pybbda/data/assets/*

clean:
	rm -fr pybbda.egg-info
	rm -fr build
	rm -fr dist
	rm -fr .pytest_cache

dist: clean
	python setup.py bdist_wheel
	python setup.py sdist

docs: install-dev
	cd docs && make html

install-dev:
	pip install --quiet -r requirements-dev.txt

install: install-dev
	pip install -e .