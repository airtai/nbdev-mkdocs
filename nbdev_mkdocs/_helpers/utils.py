# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/Utils.ipynb.

# %% auto 0
__all__ = ['set_cwd', 'get_value_from_config']

# %% ../../nbs/Utils.ipynb 1
import os
from typing import *
from contextlib import contextmanager
from pathlib import Path

import nbdev
from configparser import ConfigParser

# %% ../../nbs/Utils.ipynb 3
@contextmanager
def set_cwd(cwd_path: Union[Path, str]):

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
    """Get the value from settings.ini file"""

    settings_path = Path(root_path) / "settings.ini"
    config = ConfigParser()
    config.read(settings_path)
    if not config.has_option("DEFAULT", config_name):
        return ""
    return config["DEFAULT"][config_name]