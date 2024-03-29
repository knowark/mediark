clean:
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf ./.cache .mypy_cache ./schema/.mypy_cache .coverage

test:
	pytest

PROJECT = mediark
COVFILE ?= .coverage

mypy:
	mypy $(PROJECT)

coverage-application:
	export COVERAGE_FILE=$(COVFILE); pytest --cov-branch \
	--cov=$(PROJECT)/application tests/application/ \
	--cov-report term-missing -x -s -W ignore::DeprecationWarning \
	-o cache_dir=/tmp/mediark/cache

coverage:
	export COVERAGE_FILE=$(COVFILE); pytest --cov-branch \
	--cov=$(PROJECT) tests/ --cov-report term-missing -x -s -vv \
	-W ignore::DeprecationWarning -W ignore ./mediark/integration/core/http\
	/http_client.py -o cache_dir=/tmp/mediark/cache

serve:
	python -m $(PROJECT) serve

serve-dev:
	export mediark_MODE=DEV; python -m $(PROJECT) serve

deploy:
	ansible-playbook -c local -i localhost, setup/deploy.yml

prepare:
	bash -c \
	'source /opt/$(PROJECT)/env/bin/activate && python -m $(PROJECT) prepare'

restart:
	systemctl daemon-reload && systemctl restart $(PROJECT).target \
	&& journalctl -f

push:
	git push && git push --tags

local:
	./setup/local.sh

PART ?= patch

version:
	bump2version $(PART) $(PROJECT)/__init__.py --tag --commit

update:
	git clean -xdf
	git reset --hard
	git checkout master
	git pull --all

gitmessage:
	touch .gitmessage
	echo "\n# commit message\n.gitmessage" >> .gitignore
	git config commit.template .gitmessage
