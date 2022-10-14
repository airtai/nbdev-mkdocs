SRC = $(wildcard nbs/*.ipynb)
PACKAGE_DATA = $(wildcard package_data/*)

all: prepare

nbdev_mkdocs: $(SRC) $(PACKAGE_DATA) settings.ini Makefile
	nbdev_export
	rm -rf nbdev_mkdocs/package_data; cp -r package_data nbdev_mkdocs/
	touch nbdev_mkdocs

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

README.md: install
	nbdev_readme

# the difference between install and dist target is that dist has the latest README.md installed
dist: README.md
	python setup.py sdist bdist_wheel
	pip uninstall -y dist/nbdev_mkdocs-*-py3-none-any.whl
	pip install `ls dist/nbdev_mkdocs-*-py3-none-any.whl`\[dev\]
	touch dist

test: install
	nbdev_test
    
mypy: nbdev_mkdocs
	mypy nbdev_mkdocs --ignore-missing-imports
    
sast: .sast_bandit .sast_semgrep

.sast_bandit: nbdev_mkdocs
	bandit -r nbdev_mkdocs
	touch .sast_bandit
    
.sast_semgrep: nbdev_mkdocs
	semgrep --config auto --error nbdev_mkdocs
	touch .sast_semgrep

check_all: mypy sast test

mkdocs/site: install
	nbdev_mkdocs prepare
	touch mkdocs/site
    
preview: mkdocs/site
	nbdev_mkdocs preview

prepare: dist mkdocs/site check_all
	nbdev_clean

clean:
	rm -rf nbdev_mkdocs
	rm -rf dist
	rm -rf build
	rm -rf _proc
	rm -rf nbdev_mkdocs.egg-info
	rm -rf mkdocs/site
	pip uninstall -y nbdev_mkdocs
