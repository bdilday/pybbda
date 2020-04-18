from io import BytesIO
import os
import requests
import tempfile
import zipfile
import glob
import pathlib
import shutil
import logging

from ..lahman import LAHMAN_URL


def _download():
    logging.info("downloading file from %s", LAHMAN_URL)
    archive = zipfile.ZipFile(BytesIO(requests.get(LAHMAN_URL, stream=True).content))
    target = tempfile.gettempdir()
    archive.extractall(path=target)
    return target


def _extract(target, output_path=None):
    output_path = (
        output_path or pathlib.Path(__file__).parent.parent / "assets" / "Lahman"
    )

    if not os.path.isdir(output_path):
        raise ValueError(f"Path {output_path} must be a directory")
    extracted_files = glob.glob(os.path.join(target, "**", "*csv"), recursive=True)
    for extracted_file in extracted_files:
        shutil.copy(extracted_file, output_path)


def _update(output_path=None):
    target = _download()
    _extract(target, output_path)
