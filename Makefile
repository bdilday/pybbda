.PHONY: test lint clean dev dist

lint:
	python -m black pybaseballdatana/ tests/
	python -m flake8 pybaseballdatana

test-analysis:
	python -m pytest tests/analysis/

test-data:
	python -m pytest tests/data/

test-markov:
	python -m pybaseballdatana.analysis.run_expectancy.markov.cli \
	--batting-probs 0.1 0.1 0.1 0.1 0.1 \
	--running-probs 0.1 0.1 0.1 0.1

test:
	python -m pytest tests/


clean:
	rm -fr pybaseballdatana.egg-info
	rm -fr build
	rm -fr dist

dist: clean
	python setup.py bdist_wheel
	python setup.py sdist

docs: install-dev
	cd docs && make html

install-dev:
	pip install -r requirements-dev.txt

install: install-dev
	pip install -e .