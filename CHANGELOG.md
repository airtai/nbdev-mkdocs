# Release notes

<!-- do not remove -->

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
