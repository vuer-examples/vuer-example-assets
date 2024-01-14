# shell option to use extended glob from from https://stackoverflow.com/a/6922447/1560241
SHELL:=/bin/bash -O extglob

NEW_VERSION=`< ../vuer/VERSION`
CURR_VERSION=`< VERSION`

default: prepare-release release

prepare-release:
	@echo bumping $(CURR_VERSION) to $(NEW_VERSION)
	@echo $(VERSION)>VERSION
	-git tag -d v$(NEW_VERSION)
	-git tag -d latest
release:
	git push
	-git tag v$(NEW_VERSION)
	-git tag latest
	git push origin --tags -f
