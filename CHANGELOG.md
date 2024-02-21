# Release notes

<!-- do not remove -->

## 0.6.1

### New Features

- Create new CLI command "nbdev mkdocs readme" ([#206](https://github.com/airtai/nbdev-mkdocs/pull/206)), thanks to [@harishmohanraj](https://github.com/harishmohanraj)

### Bugs Squashed

- Do not run "nbdev_docs" while running "nbdev_mkdocs docs" ([#208](https://github.com/airtai/nbdev-mkdocs/pull/208)), thanks to [@harishmohanraj](https://github.com/harishmohanraj)

- AttributeError: module 'openai' has no attribute 'error ([#212](https://github.com/airtai/nbdev-mkdocs/issues/212)), thanks to [@harishmohanraj](https://github.com/harishmohanraj)


## 0.6.0


### New Features 

- Support for Python 3.7 has been removed. 


### Bugs Squashed

- Add correct URL to mkdocs config file when executing the social image generate CLI command ([#202](https://github.com/airtai/nbdev-mkdocs/pull/202)), thanks to [@harishmohanraj](https://github.com/harishmohanraj)

- Fix docs build failure on Windows ([#194](https://github.com/airtai/nbdev-mkdocs/pull/194)), thanks to [@harishmohanraj](https://github.com/harishmohanraj)


## 0.5.1


### Bugs Squashed

- Fix the misalignment of class methods in the documentation ([#186](https://github.com/airtai/nbdev-mkdocs/pull/186)), thanks to [@harishmohanraj](https://github.com/harishmohanraj)
- Fix build failures when the repository and exported library names differ ([#184](https://github.com/airtai/nbdev-mkdocs/pull/184)), thanks to 
[@harishmohanraj](https://github.com/harishmohanraj)


## 0.5.0

### New Features

- Replace static parsing of source files with dynamic import from library when extracting symbols ([#180](https://github.com/airtai/nbdev-mkdocs/pull/180)), thanks to 
[@harishmohanraj](https://github.com/harishmohanraj)


## 0.4.0


### Bugs Squashed

- Callout does not work ([#179](https://github.com/airtai/nbdev-mkdocs/pull/179)), thanks to [@harishmohanraj](https://github.com/harishmohanraj)


## 0.3.0


### Bugs Squashed

- Switch to chatGPT model from codex model ([#171](https://github.com/airtai/nbdev-mkdocs/issues/171))


## 0.2.2


### Bugs Squashed

- Don't run nbdev_readme automatically ([#168](https://github.com/airtai/nbdev-mkdocs/pull/168)), thanks to [@harishmohanraj](https://github.com/harishmohanraj)
  - Closes #166

## 0.2.1


### Bugs Squashed

- Load symbols dynamically and link it to the docs ([#160](https://github.com/airtai/nbdev-mkdocs/issues/160))


## 0.2.0


### Bugs Squashed

- Upgrade mkdocstrings and python handler

- Fix prepare and preview tests ([#155](https://github.com/airtai/nbdev-mkdocs/issues/155))

- Add docs version in the link to the symbols ([#151](https://github.com/airtai/nbdev-mkdocs/issues/151))

- Fix link to symbols in docs ([#144](https://github.com/airtai/nbdev-mkdocs/issues/144))
  - https://github.com/fastai/nbdev/blob/master/nbdev/doclinks.py#L87


## 0.1.0

### New Features

- Add documentation versioning ([#72](https://github.com/airtai/nbdev-mkdocs/issues/72))
  - https://squidfunk.github.io/mkdocs-material/setup/setting-up-versioning/

- add detect-secrets to pre-commit hooks ([#138](https://github.com/airtai/nbdev-mkdocs/issues/138))

- Integrate docstring-gen into nbdev-mkdocs ([#123](https://github.com/airtai/nbdev-mkdocs/issues/123))

- Rename the CLI command "nbdev_mkdocs generate-social-image" to "nbdev_mkdocs social-image generate" ([#127](https://github.com/airtai/nbdev-mkdocs/issues/127))


### Bugs Squashed

- Hide the badges displayed on the index page in the docs ([#118](https://github.com/airtai/nbdev-mkdocs/issues/118))

- nbdev docs: The CI build status badge should not appear in the documentation. ([#113](https://github.com/airtai/nbdev-mkdocs/issues/113))

- nbdev docs: Locally referenced images are not showing up in the docs ([#110](https://github.com/airtai/nbdev-mkdocs/issues/110))


## 0.0.4

### New Features

- Rename the CLI command "nbdev_mkdocs generate-social-image" to "nbdev_mkdocs social-image generate" ([#127](https://github.com/airtai/nbdev-mkdocs/issues/127))

- Integrate docstring-gen into nbdev-mkdocs ([#123](https://github.com/airtai/nbdev-mkdocs/issues/123))

### Bugs Squashed

- Hide the badges displayed on the index page in the docs ([#118](https://github.com/airtai/nbdev-mkdocs/issues/118))

- nbdev docs: The CI build status badge should not appear in the documentation. ([#113](https://github.com/airtai/nbdev-mkdocs/issues/113))

- nbdev docs: Locally referenced images are not showing up in the docs ([#110](https://github.com/airtai/nbdev-mkdocs/issues/110))



## 0.0.3

### Bugs Squashed

- CI bug fix

## 0.0.2

### New Features

- If a CLI command documentation fails, rather than failing, print the exception in the terminal. ([#107](https://github.com/airtai/nbdev-mkdocs/issues/107))

- Make API, CLI and Releases configurable in the docs ([#106](https://github.com/airtai/nbdev-mkdocs/issues/106))

- Handle glob expressions while building the navigation tree for MkDocs ([#100](https://github.com/airtai/nbdev-mkdocs/issues/100))

- Build tensorflow based Docker image with preinstalled nbdev_mkdocs and all requirements ([#95](https://github.com/airtai/nbdev-mkdocs/issues/95))

- Build docker images with preinstalled nbdev_mkdocs and all requirements ([#94](https://github.com/airtai/nbdev-mkdocs/issues/94))

- Use AI to generate social image ([#81](https://github.com/airtai/nbdev-mkdocs/issues/81))

- Read sidebar.yml for generating the docs navigation ([#62](https://github.com/airtai/nbdev-mkdocs/issues/62))

### Bugs Squashed

- Uploading large images breaks the social share image. ([#98](https://github.com/airtai/nbdev-mkdocs/issues/98))

- Copy requirements in dev-requirements for client projects and not for nbdev-mkdocs ([#79](https://github.com/airtai/nbdev-mkdocs/issues/79))

- Install mkdoc-nbdev from pypi instead of git ([#54](https://github.com/airtai/nbdev-mkdocs/issues/54))
  - The following code in deployed.yml installs the git version for all our projects, but it should do that only for the nbdev-mkdocs project:


## 0.0.1

### New Features

- Add stuffs to gitignore when you run nbdev_new ([#59](https://github.com/airtai/nbdev-mkdocs/issues/59))

- Create new repo for maintaining workflows ([#52](https://github.com/airtai/nbdev-mkdocs/issues/52))

- Call nbdev_prepare internally when calling nbdev_mkdocs prepare ([#43](https://github.com/airtai/nbdev-mkdocs/issues/43))

- Enable local development ([#36](https://github.com/airtai/nbdev-mkdocs/issues/36))

- Use quarto to convert notebooks into markdown ([#35](https://github.com/airtai/nbdev-mkdocs/pull/35)), thanks to [@harishmohanraj](https://github.com/harishmohanraj)

- Update ghp deploy action template ([#33](https://github.com/airtai/nbdev-mkdocs/pull/33)), thanks to [@harishmohanraj](https://github.com/harishmohanraj)

- Use nbdev and quarto for converting notebooks into markdown files ([#31](https://github.com/airtai/nbdev-mkdocs/issues/31))
  - - [ ] Update walkthrough docs to install quarto

- Create new deploy action as part of the nbdev-mkdocs new command ([#25](https://github.com/airtai/nbdev-mkdocs/issues/25))

- Implement logic to hide cells in guides notebook ([#24](https://github.com/airtai/nbdev-mkdocs/issues/24))

- Generate cli docs ([#14](https://github.com/airtai/nbdev-mkdocs/pull/14)), thanks to [@harishmohanraj](https://github.com/harishmohanraj)
  - Closes #4

- Add release page ([#10](https://github.com/airtai/nbdev-mkdocs/pull/10)), thanks to [@harish-airt](https://github.com/harish-airt)
  - Closes #8

- Initial commit, thanx to [@davorrunje](https://github.com/davorrunje)
