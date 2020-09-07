REQUIREMENTS_DEVELOPMENT := requirements/development.txt
REQUIREMENTS_PRODUCTION := requirements/production.txt

.PHONY: all install pip-update-setuptools pip-install-development pip-install update pre-commit-hooks test coverage clean

all: install test clean

install:
	@echo "Installing the dependencies"
	@poetry install --no-root --quiet --no-interaction

pip-update-setuptools:
	@echo "Updating the pip, setuptools and wheel packages"
	@python -m pip install pip setuptools wheel --upgrade --quiet --no-cache-dir

pip-install-development: pip-update-setuptools
	@echo "Installing the dependencies for development"
	@pip install --requirement $(REQUIREMENTS_DEVELOPMENT) --no-deps --upgrade --quiet --no-cache-dir

pip-install: pip-update-setuptools
	@echo "Installing the dependencies"
	@pip install --requirement $(REQUIREMENTS_PRODUCTION) --no-deps --upgrade --quiet --no-cache-dir

update:
	@echo "Downloading the latest versions of the dependencies"
	@poetry update --lock --quiet --no-interaction
	@poetry export --format requirements.txt --output $(REQUIREMENTS_DEVELOPMENT) --without-hashes --dev
	@poetry export --format requirements.txt --output $(REQUIREMENTS_PRODUCTION) --without-hashes --extras deployment

pre-commit-hooks:
	@echo "Running the Git hooks"
	@pre-commit run --all-files

test:
	@echo "Running the test cases"
	@coverage run manage.py test --no-input --failfast

coverage: test
	@echo "Analyzing the code coverage for all test cases"
	@coverage report
	@coverage html

clean:
	@echo "Delete all temporary files"
	@find readable tests -type f -name '*.py[cod]' | xargs rm --force
	@find readable tests -type d -name '__pycache__' | xargs rm --force --recursive
