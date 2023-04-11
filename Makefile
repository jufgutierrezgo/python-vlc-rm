# Define the name of your Python package
PKG_NAME = python-vlc-rm

# Define the list of files to include in your package
FILES = your_package_name/*.py your_package_name/data/*

# Define the list of dependencies required to build and test your package
DEPS = requirements.txt

# Define variables
PYTHON := python
COVERAGE := coverage

# Define the list of commands to run when building and testing your package
.PHONY: all
all: build test

.PHONY: build
build:
	python setup.py sdist bdist_wheel

.PHONY: test 
test:	 	

transmitter:
	pytest -s tests/test_transmitter.py

photodetector:
	pytest -s tests/test_photodetector.py

indoorenv:
	pytest -s tests/test_indoorenv.py

recursivemodel:
	pytest -s tests/test_recursivemodel.py

ser:
	pytest -s tests/test_ser.py

.PHONY: install
install:
	pip install -r $(DEPS)
	pip install --editable .

.PHONY: clean
clean:
	rm -rf dist/ build/ $(PKG_NAME).egg-info/ __pycache__/ .pytest_cache/

.PHONY: lint
lint:
	flake8 $(FILES)

.PHONY: mypy
mypy:
	mypy $(FILES)


.PHONY: coverage
coverage:
	coverage run -m pytest tests/ 
	coverage report -m

.PHONY: coverage-html
coverage: 
	coverage run -m pytest tests/ 
	
html:	
	coverage html
