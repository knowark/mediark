clean:
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf ./.cache
	rm -f .coverage
	rm -rf .mypy_cache

test:
	pytest

COVFILE ?= .coverage
PROJECT = mediark

coverage-application:
	# mypy $(PROJECT)/application
	export COVERAGE_FILE=$(COVFILE); pytest -x \
	--cov=$(PROJECT)/application tests/application/ \
	--cov-report term-missing -s -vv \
	-o cache_dir=/tmp/pytest/cache

coverage-infrastructure:
	mypy $(PROJECT)/infrastructure
	export COVERAGE_FILE=$(COVFILE); pytest -x \
	--cov=$(PROJECT)/infrastructure tests/infrastructure/ \
	--cov-report term-missing -s -vv \
	-o cache_dir=/tmp/pytest/cache

coverage: 
	mypy $(PROJECT)
	export COVERAGE_FILE=$(COVFILE); pytest -x \
	--cov=$(PROJECT) tests/ \
	--cov-report term-missing -s -vv \
	-o cache_dir=/tmp/pytest/cache

update:
	pip-review --auto
	pip freeze > requirements.txt

serve:
	python -m $(PROJECT) serve

PART ?= patch

version:
	bump2version $(PART) mediark/__init__.py --tag --commit

install-all:
	pip install -r requirements.txt

uninstall-all:
	pip freeze | xargs pip uninstall -y

upgrade:
	pip-review --local --auto
	pip freeze > requirements.txt

dev-deploy:
	 bin/dev_deploy.sh
