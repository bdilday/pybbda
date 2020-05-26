.PHONY: test test-analysis test-data test-markov lint clean install-dev install dist

lint: install-dev
	python -m black pybaseballdatana/ tests/
	python -m flake8 pybaseballdatana

test-analysis: install-dev
	python -m pytest tests/analysis/

test-data: install-dev
	python -m pytest tests/data/

test-markov: install
	python -m pybaseballdatana.analysis.run_expectancy.markov.cli \
	--batting-probs 0.1 0.1 0.1 0.1 0.1 \
	--running-probs 0.1 0.1 0.1 0.1

test: install-dev
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