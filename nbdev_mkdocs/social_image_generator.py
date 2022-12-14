# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/Social_Image_Generator.ipynb.

# %% auto 0
__all__ = ['generate_social_image']

# %% ../nbs/Social_Image_Generator.ipynb 1
from typing import *
from pathlib import Path
import re
import os
import asyncio
import shutil
from tempfile import TemporaryDirectory
from enum import Enum

import openai
import typer
from playwright.async_api import async_playwright
from ruamel.yaml import YAML

from nbdev_mkdocs._helpers.utils import (
    set_cwd,
    get_value_from_config,
    is_local_path,
    add_counter_suffix_to_filename,
)
from ._package_data import get_root_data_path

# %% ../nbs/Social_Image_Generator.ipynb 3
def _generate_ai_image(prompt: str) -> str:
    """Generate an image for social card using the OpenAI Image API.

    Args:
        prompt: The prompt to use for generating the image.

    Returns:
        The URL of the generated image.
    """
    response = openai.Image.create(prompt=prompt, n=1, size="512x512")
    image_url: str = response["data"][0]["url"]
    return image_url

# %% ../nbs/Social_Image_Generator.ipynb 5
def _generate_html_str(root_path: str, image_url: str) -> str:
    """Generate html string for the social card

    Args:
        root_path: The root path of the project.
        image_url: The image URL to be included in the HTML.
    """

    with set_cwd(root_path):

        _custom_social_image_template_path = (
            get_root_data_path() / "custom-social-image-template.html"
        )

        with open(_custom_social_image_template_path, "r") as f:
            _html_template = f.read()

        user_name = get_value_from_config(root_path, "user")
        project_name = get_value_from_config(root_path, "repo")
        project_description = get_value_from_config(root_path, "description")

        image_url = Path(image_url).name if is_local_path(image_url) else image_url

        d = dict(
            fill_in_user_name=user_name,
            fill_in_project_name=project_name,
            fill_in_project_description=project_description,
            fill_in_image_url=image_url,
        )

        for k, v in d.items():
            _html_template = _html_template.replace(k, v)

        return _html_template

# %% ../nbs/Social_Image_Generator.ipynb 8
async def _capture_and_save_screenshot(src_path: str, dst_path: str):
    """Capture screenshot of an HTML file from source directory and save the
    output in destination directory

    Args:
        src_path: The source path of the HTML file that will be used to generate the PNG image.
        dst_path: The destination path where the generated screenshot image will be saved.
    """
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch()

    try:
        page = await browser.new_page()

        html_path = Path(src_path) / "social_image.html"
        await page.goto(f"file://{str(html_path.resolve())}")

        output_path = (
            Path(dst_path) / "mkdocs" / "docs_overrides" / "images" / "social_image.png"
        )

        if output_path.exists():
            add_counter_suffix_to_filename(output_path)

        await page.locator("#container").screenshot(path=str(output_path.resolve()))

        typer.echo(f"Social share image generated and saved at: '{output_path}'")

    finally:
        await browser.close()

# %% ../nbs/Social_Image_Generator.ipynb 10
async def _create_social_image(root_path: str, image_url: str):
    """Create social image for the project

    Args:
        root_path: The root path of the project.
        image_url: The image URL to be included in the social image.
    """
    html_str = _generate_html_str(root_path, image_url)

    with TemporaryDirectory() as d:

        html_path = Path(d) / "social_image.html"
        with open(html_path, "w") as f:
            f.write(html_str)

        if is_local_path(image_url):
            shutil.copyfile(Path(image_url), Path(d) / Path(image_url).name)

        await _capture_and_save_screenshot(d, root_path)

# %% ../nbs/Social_Image_Generator.ipynb 12
def _unescape_exclamation_mark(text: str) -> str:
    """Replaces the URL-encoded `!%21` character sequence with `!!` in a string.

    Args:
        text: The string to be processed.

    Returns:
        The input string with the `!%21` character sequence replaced with `!!`.
    """
    pattern = r":\s*!%21"
    text = re.sub(pattern, r": !!", text)
    return text

# %% ../nbs/Social_Image_Generator.ipynb 14
def _update_social_image_in_mkdocs_yml(root_path: str, image_url: str):
    """Update social image link in mkdocs yml file

    Args:
        root_path: The root path of the project.
        image_url: The image URL to update in the mkdocs yml file.
    """

    image_url = (
        "overrides/images/social_image.png" if is_local_path(image_url) else image_url
    )

    yaml = YAML()
    mkdocs_yml_path = Path(root_path) / "mkdocs" / "mkdocs.yml"
    config = yaml.load(mkdocs_yml_path)
    config["extra"]["social_image"] = image_url
    yaml.dump(config, mkdocs_yml_path, transform=_unescape_exclamation_mark)

# %% ../nbs/Social_Image_Generator.ipynb 16
def _update_social_image_in_site_overrides(root_path: str, image_url: str):
    """Update social image link in site_overrides HTML template

    Args:
        root_path: The root path of the project.
        image_url: The image URL to update in the site_overrides HTML template.
    """

    _replace_str = (
        'page.canonical_url ~ "" ~ config.extra.social_image '
        if is_local_path(image_url)
        else "config.extra.social_image "
    )

    with set_cwd(root_path):
        site_overrides_path = (
            Path(root_path) / "mkdocs" / "site_overrides" / "main.html"
        )
        if not site_overrides_path.exists():
            typer.secho(
                f"Unexpected error: path {site_overrides_path.resolve()} does not exists!",
                err=True,
                fg=typer.colors.RED,
            )
            raise typer.Exit(code=1)

        with open(site_overrides_path, "r") as f:
            _new_text = f.read()
            _pattern = re.compile(r".*?{%.*?image_url = (.*)%}")
            _match = re.search(_pattern, _new_text)
            _new_text = _new_text.replace(_match.group(1), _replace_str)  # type: ignore

        with open(site_overrides_path, "w") as f:
            f.write(_new_text)

# %% ../nbs/Social_Image_Generator.ipynb 19
class _IMG_Generator(str, Enum):
    file = "file"
    dall_e = "dall_e"


def _generate_image_url(
    root_path: str, generator: str, prompt: str, image_path: Optional[str] = None
) -> str:
    """Generate image url based on the generator

    Args:
        root_path: The root path of the project.
        generator: Generator to use to create the social image. Valid options are: 'file' and 'dall_e'.
        prompt: The prompt to use for generating the image.
        image_path: Image file path to use in the social share image. If None, then the default image will be used.

    Returns:
        The image url
    """
    if generator not in _IMG_Generator._member_names_:
        raise ValueError(
            "Invalid Option for generator. Valid options are: 'file' and 'dall_e'"
        )

    elif generator == _IMG_Generator.dall_e.value:
        image_url = _generate_ai_image(prompt=prompt)

    else:
        with set_cwd(root_path):
            if image_path is not None:
                _image_path = Path(
                    os.path.normpath(Path(root_path).joinpath(image_path))
                ).resolve()

                if not _image_path.exists():
                    typer.secho(
                        f"Unexpected error: path {_image_path.resolve()} does not exists!",
                        err=True,
                        fg=typer.colors.RED,
                    )
                    raise typer.Exit(code=1)

                image_url = str(_image_path)

            else:
                image_url = str(
                    (
                        Path(root_path)
                        / "mkdocs"
                        / "docs_overrides"
                        / "images"
                        / "default_social_logo.png"
                    ).resolve()
                )

    return image_url

# %% ../nbs/Social_Image_Generator.ipynb 26
async def generate_social_image(
    root_path: str,
    generator: str = "file",
    prompt: str = "Cute animal wearing hoodie sitting in high chair in purple room, browsing computer, 3d render",
    image_path: Optional[str] = None,
):
    """Generate a custom image for social card using the OpenAI Image API.

    Args:
        root_path: The root path of the project.
        generator: Generator to use to create the social image. Valid options are: 'file' and 'dall_e'.
        prompt: The prompt to use for generating the image.
        image_path: Image file path to use in the social share image. Use images with a 1:1 aspect ratio and at least 512x512 pixels for the best results. If None, then the default image will be used.
    """

    image_url = _generate_image_url(root_path, generator, prompt, image_path)

    await _create_social_image(root_path, image_url)

    _update_social_image_in_mkdocs_yml(root_path, image_url)

    _update_social_image_in_site_overrides(root_path, image_url)
