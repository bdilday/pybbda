from io import BytesIO
import os
import requests
import tempfile
import zipfile
import glob
import pathlib
import shutil

from ..lahman import LAHMAN_URL
import logging

logger = logging.getLogger(__name__)


def _download():
    logger.info("downloading file from %s", LAHMAN_URL)
    archive = zipfile.ZipFile(BytesIO(requests.get(LAHMAN_URL, stream=True).content))
    target = tempfile.gettempdir()
    archive.extractall(path=target)
    return target


def _extract(target, output_root):
    output_path = os.path.join(output_root, "Lahman")
    os.makedirs(output_path, exist_ok=True)
    extracted_files = glob.glob(os.path.join(target, "**", "*csv"), recursive=True)
    for extracted_file in extracted_files:
        try:
            shutil.copy(extracted_file, output_path)
        except shutil.SameFileError:
            logger.warning(
                "source and destination file (%s) are the same",
                os.path.join(output_path, extracted_file),
            )


def _validate_path(output_root):
    output_root = output_root or pathlib.Path(__file__).parent.parent / "assets"
    if not os.path.exists(output_root):
        raise ValueError(f"Path {output_root} does not exist")
    if not os.path.isdir(output_root):
        raise ValueError(f"Path {output_root} must be a directory")


def _update(output_root=None):
    output_root = output_root or pathlib.Path(__file__).parent.parent / "assets"
    _validate_path(output_root)
    target = _download()
    _extract(target, output_root)
