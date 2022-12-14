# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/Docstring.ipynb.

# %% auto 0
__all__ = ['logger', 'run_examples_from_docstring']

# %% ../nbs/Docstring.ipynb 2
from typing import *
import sys
import os

import re

import textwrap
from subprocess import run, CalledProcessError  # nosec: B404
from tempfile import TemporaryDirectory
from pathlib import Path

import rich
from rich import print
from rich.console import Group, Console
from rich.panel import Panel
from rich.rule import Rule
import logging

# %% ../nbs/Docstring.ipynb 3
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# %% ../nbs/Docstring.ipynb 4
try:
    import griffe

    griffe_logger = logging.getLogger("griffe.docstrings.google")

    griffe_logger.setLevel(logging.ERROR)

    griffe_logger.warning("you should not see this")
except:  # nosec: B110:try_except_pass] Try, Except, Pass detected.
    pass

# %% ../nbs/Docstring.ipynb 6
import rich.jupyter

rich.jupyter.JUPYTER_HTML_FORMAT = """\
<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace;font-size:.68rem">{code}</pre>
"""

# logger.info(f"{rich.jupyter.JUPYTER_HTML_FORMAT=}")

# %% ../nbs/Docstring.ipynb 10
def _extract_examples_from_docstring(o: Any) -> List[str]:
    try:
        import griffe
    except:
        raise Exception(
            "This function should only be used for testing where griffe package is installed."
        )

    if o.__doc__ is None:
        raise ValueError(f"{o.__name__}.__doc__ = {o.__doc__}")
    sections = griffe.docstrings.parse(
        griffe.dataclasses.Docstring(o.__doc__), griffe.docstrings.Parser.google
    )

    def find_python_code(s: str) -> str:
        code = [x[0] for x in re.findall("```\s*python((\n|.|\\n])+)```", s)]
        #         print(f"{code=}")
        if len(code) == 0:
            raise ValueError(f"No python code found in {s}")
        return "\n\n".join(code)

    examples = [
        find_python_code(section.value.description)  # type: ignore
        for section in sections
        if section.kind.value == "admonition" and section.value.annotation == "example"  # type: ignore
    ]

    return examples

# %% ../nbs/Docstring.ipynb 15
def _get_keywords(examples: List[str]) -> List[str]:
    keywords: List[str] = sum(
        [
            [x[9:-1] for x in re.findall("{fill in \w+}", example)]
            for example in examples
        ],
        [],
    )

    return keywords

# %% ../nbs/Docstring.ipynb 17
def _replace_keywords(examples: List[str], **kwargs) -> List[str]:
    keywords = _get_keywords(examples)

    if set(keywords) > set(kwargs.keys()):
        raise ValueError(f"{set(keywords)} > {set(kwargs.keys())}")

    for keyword in keywords:
        examples = [
            example.replace("{fill in " + keyword + "}", kwargs[keyword])
            for example in examples
        ]

    return examples

# %% ../nbs/Docstring.ipynb 19
def _format_output(
    s: str,
    *,
    title: str,
    supress: bool = False,
    sub_dict: Optional[Dict[str, str]] = None,
    width: Optional[int] = None,
):
    if sub_dict:
        for pattern, replacement in sub_dict.items():
            s = re.sub(pattern, replacement, s)
    if supress:
        return Group(Rule(f"{title} supressed"), "N/A")
    #         return Panel("", title=f"{title} supressed", width=width)
    else:
        return Group(Rule(title), s)


#         return Panel(s, title=title, width=width)

# %% ../nbs/Docstring.ipynb 21
def run_examples_from_docstring(
    o: Any,
    *,
    supress_stdout: bool = False,
    supress_stderr: bool = False,
    sub_dict: Optional[Dict[str, str]] = None,
    width: Optional[int] = 80,
    **kwargs,
):
    """Runs example from a docstring

    Parses docstring of an objects looking for examples. The examples are then saved into files and executed
    in a separate process.

    Note:
        Execution context is not the same as the one in the notebook because we want examples to work from
        user code. Make sure you compiled the library prior to executing the examples, otherwise you might
        be running them agains an old version of the library.

    Args:
        o: an object, typically a function or a class, for which docstring is being parsed for examples
        supress_stdout: omit stdout from output, typically due to security considerations
        supress_stderr: omit stderr from output, typically due to security considerations
        sub_dict: a dictionary mapping regexp patterns into replacement strings used to mask stdout and
            stderr, typically used to mask sensitive information such as passwords

        **kwargs: arguments use to replace "{fill in **param**}" in docstring with the actual values when running examples

    Raises:
        ValueError: if some params are missing from the **kwargs**
        RuntimeException: if example fails

    Example:
        ```python
        from  nbdev_mkdocs.docstring import run_examples_from_docstring

        def f():
            ```python
            Example:
                print("Hello {fill in name}!")
                print("Goodbye {fill in other_name}!")
            ```
            pass


        run_examples_from_docstring(f, name="John", other_name="Jane")
        ```
    """
    console = Console(width=width)

    examples = _extract_examples_from_docstring(o)
    if len(examples) == 0:
        raise ValueError(f"No examples found in:\n{o.__doc__}")

    executable_examples = _replace_keywords(examples, **kwargs)
    for example, executable_example in zip(examples, executable_examples):
        with TemporaryDirectory() as d:
            cmd_path = (Path(d) / "example.py").absolute()
            with open(cmd_path, "w") as f:
                f.write(executable_example)
            process = run(  # nosec: B603
                [sys.executable, str(cmd_path)], capture_output=True, text=True
            )
            group = Group(
                "Example:",
                Rule("code"),
                textwrap.indent(example, " " * 4),
                _format_output(
                    process.stdout,
                    title="stdout",
                    supress=supress_stdout,
                    sub_dict=sub_dict,
                    width=width,
                ),
                _format_output(
                    process.stderr,
                    title="stderr",
                    supress=supress_stderr,
                    sub_dict=sub_dict,
                    width=width,
                ),
            )
            #             print(Panel(panel_group, width=width))
            console.print(group)
            if process.returncode != 0:
                raise RuntimeError(process.stderr)
