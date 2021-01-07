REQUIREMENTS_DEVELOPMENT := requirements/development.txt
REQUIREMENTS_PRODUCTION := requirements/production.txt

.PHONY: all install pip-update-setuptools pip-install-development pip-install freeze update isort mypy test coverage coverage-html clean

all: install clean

install:
	@echo "Installing the dependencies"
	@poetry install --no-root --no-interaction

pip-update-setuptools:
	@echo "Updating the pip, setuptools and wheel packages"
	@python -m pip install pip setuptools wheel --upgrade --force-reinstall --quiet --no-cache-dir

pip-install-development: pip-update-setuptools
	@echo "Installing the dependencies for development"
	@pip install --requirement $(REQUIREMENTS_DEVELOPMENT) --no-deps --upgrade --force-reinstall --quiet --no-cache-dir

pip-install: pip-update-setuptools
	@echo "Installing the dependencies"
	@pip install --requirement $(REQUIREMENTS_PRODUCTION) --no-deps --upgrade --force-reinstall --quiet --no-cache-dir

freeze:
	@echo "Downloading the latest versions of the dependencies"
	@poetry update --lock --no-interaction
	@poetry export --format requirements.txt --output $(REQUIREMENTS_DEVELOPMENT) --dev
	@poetry export --format requirements.txt --output $(REQUIREMENTS_PRODUCTION) --extras deployment
	@dos2unix --keepdate --quiet $(REQUIREMENTS_DEVELOPMENT) $(REQUIREMENTS_PRODUCTION)

update: freeze install

isort:
	@echo "Trying to check correct ordering of imports"
	@isort readable tests manage.py --check-only

mypy:
	@echo "Running the static type checker"
	@mypy --config-file mypy.ini readable tests manage.py

test:
	@echo "Running the test cases"
	@coverage run manage.py test --no-input --failfast

coverage: test
	@echo "Analyzing the code coverage for all test cases"
	@coverage report

coverage-html: test
	@echo "Create an HTML report of the code coverage"
	@coverage html

clean:
	@echo "Delete all temporary files"
	@find readable tests -type f -name '*.py[cod]' | xargs rm --force
	@find readable tests -type d -name '__pycache__' | xargs rm --force --recursive
