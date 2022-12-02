Getting Started
================

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

![GitHub Workflow
Status](https://img.shields.io/github/workflow/status/airtai/nbdev-mkdocs/CI?logo=GitHub.png)
![PyPI - Python
Version](https://img.shields.io/pypi/pyversions/nbdev-mkdocs.png)
![PyPI](https://img.shields.io/pypi/v/nbdev-mkdocs.png)

------------------------------------------------------------------------

**Material for nbdev** is a
<a href="https://nbdev.fast.ai/" target="_blank">nbdev</a> extension
that allows you to use
<a href="https://squidfunk.github.io/mkdocs-material/" target="_blank">Material
for MkDocs</a> to generate documentation for nbdev projects.

## Workflow

Here’s a quick comparison of Quarto and Material for nbdev development
workflows:

<!-- | **Quarto workflow**  | **Material for nbdev workflow**   |
|---    |---    |
| Install:<br>> pip install notebook nbdev<br>> nbdev_install_quarto    | Install:<br>> pip install notebook nbdev<br>> nbdev_install_quarto<br>**> pip install nbdev-mkdocs**  |
| Setup:<br>> nbdev_new<br>> nbdev_install_hooks<br>> vi settings.ini<br>> pip install -e '.[dev]'  | Setup:<br>> nbdev_new<br>> nbdev_install_hooks<br>> vi settings.ini<br>> pip install -e '.[dev]'<br>**> nbdev_mkdocs new**<br>**> vi mkdocs/mkdocs.yml**  |
| Development:<br># Edit files<br>> nbdev_preview   | Development:<br># Edit files<br>**> nbdev_mkdocs preview**<br>    |
| Commit changes:<br>> nbdev_prepare<br>> git commit -am “Commit message”<br>> git push     | Commit changes:<br>**> nbdev_mkdocs prepare**<br>> git commit -am “Commit message”<br>> git push  | -->
<table>
<thead>
<tr>
<th>
<strong>Quarto workflow</strong>
</th>
<th>
<strong>Material for nbdev workflow</strong>
</th>
</tr>
</thead>
<tbody>
<tr>
<td>

Install:

``` shell
$ pip install notebook nbdev
$ nbdev_install_quarto
```

</td>
<td>

Install:

``` shell
$ pip install notebook nbdev
$ nbdev_install_quarto
$ pip install nbdev-mkdocs
```

</td>
</tr>
<tr>
<td>

Setup:

``` shell
$ nbdev_new
$ nbdev_install_hooks
$ vi settings.ini
$ pip install -e '.[dev]'
```

</td>
<td>

Setup:

``` shell
$ nbdev_new
$ nbdev_install_hooks
$ vi settings.ini
$ pip install -e '.[dev]'
$ nbdev_mkdocs new
$ vi mkdocs/mkdocs.yml
```

</td>
</tr>
<tr>
<td>

Development:

``` shell
# Edit files
$ nbdev_preview
```

</td>
<td>

Development:

``` shell
# Edit files
$ nbdev_mkdocs preview
```

</td>
</tr>
<tr>
<td>

Commit changes:

``` shell
$ nbdev_prepare
$ git commit -am “Commit message”
$ git push
```

</td>
<td>

Commit changes:

``` shell
$ nbdev_mkdocs prepare
$ git commit -am “Commit message”
$ git push
```

</td>
</tr>
</tbody>
</table>

## Quick start

The following quick start guide will walk you through installing and
configuring nbdev-mkdocs for an existing nbdev project. It also assumes
you’ve already initialized your project with nbdev and installed all of
the required libraries.

For detailed installation instructions and configuration options, please
see the
<a href="https://nbdev-mkdocs.airt.ai/guides/Guide_01_End_To_End_Walkthrough/">End-To-End
Walkthrough</a>.

### Install

nbdev-mkdocs is published as a Python package and can be installed with
pip:

``` shell
pip install nbdev-mkdocs
```

Note that `nbdev-mkdocs` must be installed in the same Python
environment as nbdev.

If the installation was successful, you should now have the
**nbdev-mkdocs** installed on your system. Run the below command from
the terminal to see the full list of available commands:

``` shell
nbdev_mkdocs --help
```

                                                                                    
     Usage: nbdev_mkdocs [OPTIONS] COMMAND [ARGS]...                                
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --install-completion          Install completion for the current shell.      │
    │ --show-completion             Show completion for the current shell, to copy │
    │                               it or customize the installation.              │
    │ --help                        Show this message and exit.                    │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ───────────────────────────────────────────────────────────────────╮
    │ docs     Prepares files in **mkdocs/docs** and then runs **mkdocs build**    │
    │          command on them                                                     │
    │ new      Creates files in **mkdocs** subdirectory needed for other           │
    │          **nbdev_mkdocs** subcommands                                        │
    │ prepare  Runs tests and prepares files in **mkdocs/docs** and then runs      │
    │          **mkdocs build** command on them                                    │
    │ preview  Prepares files in **mkdocs/docs** and then runs **mkdocs serve**    │
    │          command on them                                                     │
    ╰──────────────────────────────────────────────────────────────────────────────╯

### Setup

After installing nbdev-mkdocs, bootstrap your project documentation by
executing the following command from the project’s root directory:

``` shell
nbdev_mkdocs new
```

Using information from the project’s settings.ini file, the above
command creates files and directories required to build the
documentation and saves it in the **mkdocs** subdirectory.

Note: You should only run the **nbdev_mkdocs new** command once for the
project to initialise the files required for building Material for
MkDocs documentation.

### Preview changes

nbdev_mkdocs lets you preview your changes as you write your
documentation. Execute the following command from the project root
directory to start a local server, and preview your documentation:

**Note**: If you haven’t already installed your library locally, run
`pip install -e '.[dev]'` command before running the
`nbdev_mkdocs prepare` command.

``` shell
nbdev_mkdocs preview
```

### Prepare changes

We recommend running the `nbdev_mkdocs prepare` command in the terminal
before committing to Git, which exports the library, tests and cleans
notebooks, and generates the README file if necessary.

``` shell
nbdev_mkdocs prepare
```

Finally, double-check your settings.ini file to ensure that it has all
of the correct information. Then commit and push your additions to
GitHub:

``` shell
git commit -am'Commit Message'
git push
```

## Copyright

Copyright © 2022 onwards airt technologies ltd, Inc.

## License

This project is licensed under the terms of the [Apache License
2.0](https://github.com/airtai/nbdev-mkdocs/blob/main/LICENSE)
