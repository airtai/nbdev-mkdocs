SRC = $(wildcard nbs/*.ipynb)
PACKAGE_DATA = $(wildcard package_data/*)

all: prepare

nbdev_mkdocs: $(SRC) $(PACKAGE_DATA) settings.ini Makefile
	nbdev_export
	pip install -e '.[dev]'
	rm -rf nbdev_mkdocs/package_data; cp -r package_data nbdev_mkdocs/
	touch nbdev_mkdocs

.PHONY: mypy
mypy: nbdev_mkdocs
	mypy nbdev_mkdocs --ignore-missing-imports

.PHONY: sast
sast: .sast_bandit .sast_semgrep

.sast_bandit: nbdev_mkdocs
	bandit -r nbdev_mkdocs
	touch .sast_bandit

.sast_semgrep: nbdev_mkdocs
	semgrep --config auto --error nbdev_mkdocs
	touch .sast_semgrep

.PHONY: static_check
static_check: mypy sast

.PHONY: prepare
prepare: static_check
	nbdev_mkdocs prepare

.PHONY: preview
preview: nbdev_mkdocs
	nbdev_mkdocs preview

.PHONY: clean
clean:
	rm -rf nbdev_mkdocs
	rm -rf dist
	rm -rf build
	rm -rf _proc
	rm -rf _docs
	rm -rf nbdev_mkdocs.egg-info
	rm -rf mkdocs/site
	# rm -rf mkdocs/docs
	rm -rf mkdocs/summary_template.txt
	pip uninstall -y nbdev_mkdocs
	touch nbs/*.ipynb
