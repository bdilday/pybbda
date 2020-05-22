.PHONY: test lint clean dev dist

lint:
	black pybaseballdatana/ tests/
	python -m flake8 pybaseballdatana

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
	cd doc && make html

install-dev:
	pip install -r requirements-dev.txt

install: install-dev
	pip install -e .