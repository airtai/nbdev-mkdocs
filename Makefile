SRC = $(wildcard nbs/*.ipynb)
PACKAGE_DATA = $(wildcard package_data/*)

all: prepare

nbdev_mkdocs: $(SRC) $(PACKAGE_DATA) settings.ini Makefile
	nbdev_export
	rm -rf nbdev_mkdocs/package_data; cp -r package_data nbdev_mkdocs/
	touch nbdev_mkdocs

.PHONY: install
install: .local_install .local_reinstall 

# install wheel locally, but don't reinstall dependancies
.local_install: nbdev_mkdocs MANIFEST.in setup.py
	python setup.py sdist bdist_wheel
	pip uninstall -y dist/nbdev_mkdocs-*-py3-none-any.whl
	pip install `ls dist/nbdev_mkdocs-*-py3-none-any.whl`\[dev\]
	touch .local_install

# install wheel locally together with its dependancies
.local_reinstall: settings.ini
	pip install --force-reinstall `ls dist/nbdev_mkdocs-*-py3-none-any.whl`\[dev\]
	touch .local_reinstall

README.md: .local_install .local_reinstall
	nbdev_readme
	# nbdev_readme is supposed to move index.md from _proc to the root dir. Currently, it is not bcz
	# of bug in the code (underlying quarto api changed)
	# Until the issue is fixed, we need to manually copy the file to the root dir.
	# Once the bug is fixed in nbdev, the below line will fail, saying "No such file or directory."
	cp _proc/README.md .

# the difference between install and dist target is that dist has the latest README.md installed
dist: README.md
	python setup.py sdist bdist_wheel
	pip uninstall -y dist/nbdev_mkdocs-*-py3-none-any.whl
	pip install `ls dist/nbdev_mkdocs-*-py3-none-any.whl`\[dev\]
	touch dist

.PHONY: test
test: install
	nbdev_test
    
.PHONY: mypy
mypy: install
	mypy nbdev_mkdocs --ignore-missing-imports
    
.PHONY: sast
sast: .sast_bandit .sast_semgrep

.sast_bandit: install
	bandit -r nbdev_mkdocs
	touch .sast_bandit
    
.sast_semgrep: install
	semgrep --config auto --error nbdev_mkdocs
	touch .sast_semgrep

.PHONY: static_check
static_check: mypy sast

.PHONY: check_all
check_all: static_check test

.PHONY: new
new: dist
	nbdev_mkdocs new
    
mkdocs/site: dist new
	nbdev_mkdocs prepare
	touch mkdocs/site
    
.PHONY: preview
preview: mkdocs/site
	nbdev_mkdocs preview

.PHONY: prepare
prepare: dist mkdocs/site check_all
	nbdev_clean

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
