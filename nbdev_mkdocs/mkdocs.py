# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/Mkdocs.ipynb.

# %% auto 0
__all__ = ['new', 'get_submodules', 'generate_api_doc_for_submodule', 'generate_api_docs_for_module', 'build_summary',
           'copy_cname_if_needed', 'prepare', 'preview']

# %% ../nbs/Mkdocs.ipynb 1
from typing import *

import os
import re
import collections
from pathlib import Path
import textwrap
import shutil
import types
import pkgutil
import importlib
import subprocess  # nosec: B404

import typer

from configupdater import ConfigUpdater, Section
from configupdater.option import Option

from configparser import ConfigParser

from nbdev.serve import proc_nbs
import nbconvert

from ._package_data import get_root_data_path

# %% ../nbs/Mkdocs.ipynb 5
def _add_requirements_to_settings(root_path: str):
    """Adds requirments needed for mkdocs to settings.ini

    Params:
        root_path: path to where the settings.ini file is located

    """
    _requirements_path = get_root_data_path() / "requirements.txt"
    with open(_requirements_path, "r") as f:
        _new_req_to_add = f.read()
        lines = _new_req_to_add.split("\n")
        lines = [s.strip() for s in lines]
        lines = [s for s in lines if s != ""]
        _new_req_to_add = " \\\n".join(lines)

    setting_path = Path(root_path) / "settings.ini"
    if not setting_path.exists():
        typer.secho(
            f"Path '{setting_path.resolve()}' does not exists! Please use --root_path option to set path to setting.ini file.",
            err=True,
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    try:

        updater = ConfigUpdater()
        updater.read(setting_path)
    except Exception as e:
        typer.secho(
            f"Error while reading '{setting_path.resolve()}': {e}",
            err=True,
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=2)

    try:
        if "requirements" not in updater["DEFAULT"]:
            updater["DEFAULT"]["requirements"] = ""

        old_req: str = updater["DEFAULT"]["requirements"].value  # type: ignore

        def remove_leading_spaces(s: str) -> str:
            return "\n".join([x.lstrip() for x in s.split("\n")])

        old_req = remove_leading_spaces(old_req)
        new_req = remove_leading_spaces(_new_req_to_add)
        if new_req in old_req:
            typer.secho(f"Requirements already added to '{setting_path.resolve()}'.")
            return

        req = old_req + " \\\n" + new_req
        req = textwrap.indent(req, " " * 4)

        req_option = Option(key="requirements", value=req)
        updater["DEFAULT"]["requirements"] = req_option
    except Exception as e:
        typer.secho(
            f"Error while updating requiremets in '{setting_path.resolve()}': {e}",
            err=True,
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=3)

    updater.update_file()

    typer.secho(f"Requirements added to '{setting_path.resolve()}'.")

    return

# %% ../nbs/Mkdocs.ipynb 8
def _create_mkdocs_dir(root_path: str):
    mkdocs_template_path = get_root_data_path() / "mkdocs_template"
    if not mkdocs_template_path.exists():
        typer.secho(
            f"Unexpected error: path {mkdocs_template_path.resolve()} does not exists!",
            err=True,
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=4)
    dst_path = Path(root_path) / "mkdocs"
    if dst_path.exists():
        typer.secho(
            f"Directory {dst_path.resolve()} already exist, skipping its creation.",
        )
    else:
        shutil.copytree(mkdocs_template_path, dst_path)
        #         shutil.move(dst_path.parent / "mkdocs_template", dst_path)
        typer.secho(
            f"Directory {dst_path.resolve()} created.",
        )

# %% ../nbs/Mkdocs.ipynb 11
_mkdocs_template_path = get_root_data_path() / "mkdocs_template.yml"

# %% ../nbs/Mkdocs.ipynb 13
with open(_mkdocs_template_path, "r") as f:
    _mkdocs_template = f.read()

# %% ../nbs/Mkdocs.ipynb 15
def _get_kwargs_from_settings(
    settings_path: Path, mkdocs_template: Optional[str] = None
) -> Dict[str, str]:
    config = ConfigParser()
    config.read(settings_path)
    if not mkdocs_template:
        mkdocs_template = _mkdocs_template
    keys = [s[1:-1] for s in re.findall("\{.*?\}", _mkdocs_template)]
    kwargs = {k: config["DEFAULT"][k] for k in keys}
    return kwargs

# %% ../nbs/Mkdocs.ipynb 17
def _create_mkdocs_yaml(root_path: str):
    try:
        # create mkdocs folder if necessary
        mkdocs_path = Path(root_path) / "mkdocs" / "mkdocs.yml"
        mkdocs_path.parent.mkdir(exist_ok=True)
        # mkdocs.yml already exists, just return
        if mkdocs_path.exists():
            typer.secho(
                f"Path '{mkdocs_path.resolve()}' exists, skipping generation of it."
            )
            return

        # get default values from settings.ini
        settings_path = Path(root_path) / "settings.ini"
        kwargs = _get_kwargs_from_settings(settings_path)
        mkdocs_yaml_str = _mkdocs_template.format(**kwargs)
        with open(mkdocs_path, "w") as f:
            f.write(mkdocs_yaml_str)
            typer.secho(f"File '{mkdocs_path.resolve()}' generated.")
            return
    except Exception as e:
        typer.secho(
            f"Unexpected Error while creating '{mkdocs_path.resolve()}': {e}",
            err=True,
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=3)

# %% ../nbs/Mkdocs.ipynb 20
_summary_template = """- [Home](index.md)
{guides}
{api}
{cli}
- [Releases](RELEASE.md)
"""


def _create_summary_template(root_path: str):
    try:
        # create mkdocs folder if necessary
        summary_template_path = Path(root_path) / "mkdocs" / "summary_template.txt"
        summary_template_path.parent.mkdir(exist_ok=True)
        # summary_template_path.yml already exists, just return
        if summary_template_path.exists():
            typer.secho(
                f"Path '{summary_template_path.resolve()}' exists, skipping generation of it."
            )
            return

        # get default values from settings.ini
        with open(summary_template_path, "w") as f:
            f.write(_summary_template)
            typer.secho(f"File '{summary_template_path.resolve()}' generated.")
            return
    except Exception as e:
        typer.secho(
            f"Unexpected Error while creating '{summary_template_path.resolve()}': {e}",
            err=True,
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=3)

# %% ../nbs/Mkdocs.ipynb 23
def new(root_path: str):
    """Initialize mkdocs project files

    Creates **mkdocs** directory in the **root_path** directory and populates
    it with initial values. You should edit mkdocs.yml file to customize it if
    needed.

    Params:
        root_path: path under which mkdocs directory will be created
    """
    _add_requirements_to_settings(root_path)
    _create_mkdocs_dir(root_path)
    _create_mkdocs_yaml(root_path)
    _create_summary_template(root_path)

# %% ../nbs/Mkdocs.ipynb 29
def _generate_markdown_from_nbs(root_path: str):
    doc_path = Path(root_path) / "mkdocs" / "docs"
    doc_path.mkdir(exist_ok=True, parents=True)

    cache = proc_nbs()
    notebooks = list(cache.glob("**/*.ipynb"))
    print(f"{cache=}")
    print(f"{notebooks=}")

    converter = nbconvert.MarkdownExporter()
    for nb in notebooks:
        body, _ = converter.from_filename(nb)
        dir_prefix = str(nb.parent)[len(str(cache)) + 1 :]
        md = doc_path / f"{dir_prefix}" / f"{nb.stem}.md"
        md.parent.mkdir(parents=True, exist_ok=True)
        with open(md, mode="w") as f:
            typer.secho(
                f"File '{md.resolve()}' created.",
            )
            f.write(body)

# %% ../nbs/Mkdocs.ipynb 32
def _generate_summary_for_guides(root_path: str) -> str:
    doc_path = Path(root_path) / "mkdocs" / "docs"
    mds = [md for md in doc_path.glob("**/*.md") if md.name.lower().startswith("guide")]

    i = len(doc_path.parts)
    if len(mds) > 0:
        return "- Guides\n    - " + "    - ".join(
            [f"[{md.stem.replace('_', ' ')}]({'/'.join(md.parts[i:])})" for md in mds]
        )
    else:
        return ""

# %% ../nbs/Mkdocs.ipynb 36
def get_submodules(package_name: str) -> List[str]:
    # nosemgrep: python.lang.security.audit.non-literal-import.non-literal-import
    m = importlib.import_module(package_name)
    submodules = [
        info.name
        for info in pkgutil.walk_packages(m.__path__, prefix=f"{package_name}.")
    ]
    submodules = [
        x
        for x in submodules
        if not any([name.startswith("_") for name in x.split(".")])
    ]
    return submodules

# %% ../nbs/Mkdocs.ipynb 38
def generate_api_doc_for_submodule(root_path: str, submodule: str) -> str:
    subpath = "API/" + submodule.replace(".", "/") + ".md"
    path = Path(root_path) / "mkdocs" / "docs" / subpath
    path.parent.mkdir(exist_ok=True, parents=True)
    with open(path, "w") as f:
        f.write(f"::: {submodule}")
    subnames = submodule.split(".")
    if len(subnames) > 2:
        return " " * 4 * (len(subnames) - 2) + f"- [{subnames[-1]}]({subpath})"
    else:
        return f"- [{submodule}]({subpath})"


def generate_api_docs_for_module(root_path: str, module_name: str) -> str:
    submodules = get_submodules(module_name)
    shutil.rmtree(Path(root_path) / "mkdocs" / "docs" / "API", ignore_errors=True)
    submodule_summary = "\n".join(
        [
            generate_api_doc_for_submodule(root_path=root_path, submodule=x)
            for x in submodules
        ]
    )
    return "- API\n" + textwrap.indent(submodule_summary, prefix=" " * 4)

# %% ../nbs/Mkdocs.ipynb 41
def build_summary(
    root_path: str,
    module: str,
):
    # create docs_path if needed
    docs_path = Path(root_path) / "mkdocs" / "docs"
    docs_path.mkdir(exist_ok=True)

    # copy README.md as index.md
    shutil.copy(Path(root_path) / "README.md", docs_path / "index.md")

    # generate markdown files
    _generate_markdown_from_nbs(root_path)

    # generates guides
    guides = _generate_summary_for_guides(root_path)

    # generate API
    api = generate_api_docs_for_module(root_path, module)

    # generate CLI
    cli = """- CLI
    - [CLI 1](index.md)"""

    # copy RELEASE.md as RELEASE.md
    shutil.copy(Path(root_path) / "RELEASE.md", docs_path / "RELEASE.md")

    # read summary template from file
    with open(Path(root_path) / "mkdocs" / "summary_template.txt") as f:
        summary_template = f.read()

    summary = summary_template.format(guides=guides, api=api, cli=cli)
    summary = "\n".join(
        [l for l in [l.rstrip() for l in summary.split("\n")] if l != ""]
    )

    with open(docs_path / "SUMMARY.md", mode="w") as f:
        f.write(summary)

# %% ../nbs/Mkdocs.ipynb 44
def copy_cname_if_needed(root_path: str):
    cname_path = Path(root_path) / "CNAME"
    dst_path = Path(root_path) / "mkdocs" / "docs" / "CNAME"
    if cname_path.exists():
        dst_path.parent.mkdir(exist_ok=True, parents=True)
        shutil.copyfile(cname_path, dst_path)
        typer.secho(
            f"File '{cname_path.resolve()}' copied to '{dst_path.resolve()}'.",
        )
    else:
        typer.secho(
            f"File '{cname_path.resolve()}' not found, skipping copying..",
        )

# %% ../nbs/Mkdocs.ipynb 47
def prepare(root_path: str):
    """Prepares mkdocs for serving

    Params:
        root_path: path under which mkdocs directory will be created
    """
    # copy cname if it exists
    copy_cname_if_needed(root_path)

    # get lib name from settings.ini
    settings_path = Path(root_path) / "settings.ini"
    config = ConfigParser()
    config.read(settings_path)
    lib_name = config["DEFAULT"]["lib_name"]
    lib_path = config["DEFAULT"]["lib_path"]

    build_summary(root_path, lib_path)

    cmd = f"mkdocs build -f {root_path}/mkdocs/mkdocs.yml"

    # nosemgrep: python.lang.security.audit.subprocess-shell-true.subprocess-shell-true
    sp = subprocess.run(  # nosec: B602:subprocess_popen_with_shell_equals_true
        cmd,
        shell=True,
        #         check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    print(sp.stdout)
    if sp.returncode != 0:
        typer.secho(
            f"Command '{cmd}' failed!",
            err=True,
            fg=typer.colors.RED,
        )
        raise typer.Exit(5)

# %% ../nbs/Mkdocs.ipynb 50
import shlex


def preview(root_path: str, port: Optional[int] = None):
    """Previes mkdocs documentation

    Params:
        root_path: path under which mkdocs directory will be created
        port: port to use
    """
    cmd = f"mkdocs serve -f {root_path}/mkdocs/mkdocs.yml -a 0.0.0.0"
    if port:
        cmd = cmd + f":{port}"

    with subprocess.Popen(  # nosec B603:subprocess_without_shell_equals_true
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        bufsize=1,
        text=True,
        universal_newlines=True,
    ) as p:
        for line in p.stdout:  # type: ignore
            print(line, end="")

    if p.returncode != 0:
        typer.secho(
            f"Command '{cmd}' failed!",
            err=True,
            fg=typer.colors.RED,
        )
        raise typer.Exit(6)
