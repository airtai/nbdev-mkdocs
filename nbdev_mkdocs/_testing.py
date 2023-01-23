# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/Testing.ipynb.

# %% auto 0
__all__ = ['openai_Image_mock', 'mock_openai_Image_create', 'mock_openai_Image_create_for_notebook']

# %% ../nbs/Testing.ipynb 1
import unittest.mock
from contextlib import contextmanager
from typing import *

# %% ../nbs/Testing.ipynb 3
@contextmanager
def mock_openai_Image_create() -> Generator[None, None, None]:
    mock = unittest.mock.MagicMock
    mock_response = unittest.mock.MagicMock
    mock_response.return_value = [
        {
            "url": "https://github.com/airtai/nbdev-mkdocs/raw/main/mkdocs/docs_overrides/images/default_social_logo.png"
        }
    ]
    mock.create = mock_response

    with unittest.mock.patch("openai.Image") as MockClass:
        MockClass.create = mock
        yield


openai_Image_mock = mock_openai_Image_create()


def mock_openai_Image_create_for_notebook():
    global openai_Image_mock

    openai_Image_mock.__enter__()
