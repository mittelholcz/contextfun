SHELL:=/bin/bash


all:
	@echo 'Choose a target:'
	@echo '    dev: update development environment, start vscode in virtualenv'
	@echo '    test: run pytest'
	@echo '    release_patch: publish new patch version'
	@echo '    release_minor: publish new minor version'
	@echo '    release_major: publish new major version'
.PHONY: all


dev: Pipfile
	@MYPYTHON=python$$(grep 'python_version' Pipfile | sed -r 's/.*"([^"]+)"/\1/') ; \
	[ $$(which $$MYPYTHON) ] || { echo "install $$MYPYTHON" ; exit 1 ; }
	@[ $$(which pipenv) ] || { echo "install pipenv" ; exit 1 ; }
	@pipenv update --dev
	@[ $$(which code) ] && pipenv run code .
.PHONY: dev


test: Pipfile
	@clear
	@pipenv run pytest --verbose test/
.PHONY: test


build: clean
	pipenv run python3 setup.py sdist bdist_wheel
.PHONY: build


clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
.PHONY: clean


OLDVER:=$$(grep -P -o "(?<=version=')[^']+" setup.py)

MAJOR:=$$(echo $(OLDVER) | sed -r s"/([0-9]+)\.([0-9]+)\.([0-9]+)/\1/")
MINOR:=$$(echo $(OLDVER) | sed -r s"/([0-9]+)\.([0-9]+)\.([0-9]+)/\2/")
PATCH:=$$(echo $(OLDVER) | sed -r s"/([0-9]+)\.([0-9]+)\.([0-9]+)/\3/")

NEWMAJORVER="$$(( $(MAJOR)+1 )).0.0"
NEWMINORVER="$(MAJOR).$$(( $(MINOR)+1 )).0" 
NEWPATCHVER="$(MAJOR).$(MINOR).$$(( $(PATCH)+1 ))"


release_major:
	@make -s __release NEWVER=$(NEWMAJORVER)
.PHONY: release_major


release_minor:
	@make -s __release NEWVER=$(NEWMINORVER)
.PHONY: release_minor


release_patch:
	@make -s __release NEWVER=$(NEWPATCHVER)
.PHONY: release_patch


__release:
	@if [[ -z "$(NEWVER)" ]] ; then \
		echo 'Do not call this target!' ; \
		echo 'Use "release_major", "release_minor" or "release_patch"!' ; \
		exit 1 ; \
		fi
	@if [[ $$(git status --porcelain) ]] ; then \
		echo 'Working dir is dirty!' ; \
		exit 1 ; \
		fi
	@echo "NEW VERSION: $(NEWVER)"
	@pipenv run pytest -q test/
	@sed -i -r "s/pypi-$(OLDVER)/pypi-$(NEWVER)/" README.md
	@sed -i -r "s/version='$(OLDVER)'/version='$(NEWVER)'/" setup.py
	@make -s build
	@git add README.md setup.py
	@git commit -m'new release'
	@git tag -a $(NEWVER) -m'release: $(NEWVER)'
	git push origin $(NEWVER)
	pipenv run python3 -m twine upload dist/*
.PHONY: __release
