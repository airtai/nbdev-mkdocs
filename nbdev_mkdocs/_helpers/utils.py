# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/Utils.ipynb.

# %% auto 0
__all__ = ['set_cwd', 'get_value_from_config', 'is_local_path', 'add_counter_suffix_to_filename', 'raise_error_and_exit']

# %% ../../nbs/Utils.ipynb 1
import os
from configparser import ConfigParser
from contextlib import contextmanager
from pathlib import Path
from typing import *
from urllib.parse import urlparse

import nbdev
import typer

# %% ../../nbs/Utils.ipynb 3
@contextmanager
def set_cwd(cwd_path: Union[Path, str]) -> Generator:
    """Set the current working directory for the duration of the context manager.

    Args:
        cwd_path: The path to the new working directory.

    !!! note

        The above docstring is autogenerated by docstring-gen library (https://github.com/airtai/docstring-gen)
    """
    cwd_path = Path(cwd_path)
    original_cwd = os.getcwd()
    os.chdir(cwd_path)

    try:
        nbdev.config.get_config.cache_clear()
        yield
    finally:
        os.chdir(original_cwd)

# %% ../../nbs/Utils.ipynb 5
def get_value_from_config(root_path: str, config_name: str) -> str:
    """Get a value from the configuration file.

    Args:
        root_path: The root path of the configuration file.
        config_name: The name of the configuration to get.

    Returns:
        The value of the configuration.

    !!! note

        The above docstring is autogenerated by docstring-gen library (https://github.com/airtai/docstring-gen)
    """
    settings_path = Path(root_path) / "settings.ini"
    config = ConfigParser()
    config.read(settings_path)
    if not config.has_option("DEFAULT", config_name):
        return ""
    return config["DEFAULT"][config_name]

# %% ../../nbs/Utils.ipynb 7
def is_local_path(path: str) -> bool:
    # Check if the path is an absolute path
    """Check if a path is a local path.

    Args:
        path: The path to check.

    Returns:
        True if the path is a local path, False otherwise.

    !!! note

        The above docstring is autogenerated by docstring-gen library (https://github.com/airtai/docstring-gen)
    """
    if os.path.isabs(path):
        return True

    # Check if the path is a URL with a scheme (e.g. http, https, ftp)
    parsed_url = urlparse(path)
    if parsed_url.scheme:
        return False

    # If the path is not an absolute path and does not have a URL scheme,
    # it is assumed to be a local path
    return True

# %% ../../nbs/Utils.ipynb 9
def add_counter_suffix_to_filename(src_path: Path) -> None:
    """Add a counter suffix to the given file

    Args:
        src_path: Path to the file to be renamed

    Returns:
        None

    !!! note

        The above docstring is autogenerated by docstring-gen library (https://github.com/airtai/docstring-gen)
    """
    parent_dir = src_path.parent
    counter_suffix = (
        max(
            [
                int(f.stem.split(".")[1])
                for f in parent_dir.glob(f"{src_path.stem}.*.*")
            ],
            default=0,
        )
        + 1
    )
    dst_path = parent_dir / f"{src_path.stem}.{counter_suffix}{src_path.suffix}"
    os.rename(src_path, dst_path)

# %% ../../nbs/Utils.ipynb 12
def raise_error_and_exit(message: str) -> None:
    """Raise an error and exit

    Args:
        message: The error message to display

    Returns:
        None

    Raises:
        typer.Exit: If the error message is not provided

    !!! note

        The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
    """
    typer.secho(
        message,
        err=True,
        fg=typer.colors.RED,
    )
    raise typer.Exit(code=1)
