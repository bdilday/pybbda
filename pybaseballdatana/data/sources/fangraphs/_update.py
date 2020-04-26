import os
import requests
import tempfile
import zipfile
import glob
import pathlib
import shutil

from bs4 import BeautifulSoup

from pybaseballdatana import logger

from ..lahman import LAHMAN_URL
import logging
logger = logging.getLogger(__name__)


def _download():
    logger.info("downloading file from %s", LAHMAN_URL)
    archive = zipfile.ZipFile(BytesIO(requests.get(LAHMAN_URL, stream=True).content))
    target = tempfile.gettempdir()
    archive.extractall(path=target)
    return target


def _save(lines, file_name, output_path):
    output_file_path = os.path.join(output_path, file_name)
    output_payload = "\n".join(str(line, "utf-8") for line in lines)
    logger.info("saving file to {}".format(output_file_path))
    with gzip.open(output_file_path, "wb") as fh:
        fh.write(bytes(output_payload, encoding="utf-8"))

def _validate_path(output_root):
    output_root = (
        output_root or pathlib.Path(__file__).parent.parent / "assets"
    )
    if not os.path.exists(output_root):
        raise ValueError(f"Path {output_root} does not exist")
    if not os.path.isdir(output_root):
        raise ValueError(f"Path {output_root} must be a directory")

def _update(output_root=None):
    output_root = (
        output_root or pathlib.Path(__file__).parent.parent / "assets"
    )
    _validate_path(output_root)
    target = _download()
    _save(target, output_root)
