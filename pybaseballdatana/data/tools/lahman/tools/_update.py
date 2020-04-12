from io import BytesIO
import os
import requests
import tempfile
import zipfile
import glob
import pathlib
import shutil
import logging

LAHMAN_URL = "https://github.com/chadwickbureau/baseballdatabank/archive/master.zip"


def _download():
    logging.info("downloading file from %s", LAHMAN_URL)
    archive = zipfile.ZipFile(BytesIO(requests.get(LAHMAN_URL, stream=True).content))
    target = tempfile.gettempdir()
    archive.extractall(path=target)
    return target


def _extract(target):
    output_path = pathlib.Path(__file__).parent / "Lahman"
    extracted_files = glob.glob(os.path.join(target, "**", "*csv"), recursive=True)
    for extracted_file in extracted_files:
        shutil.copy(extracted_file, output_path)


def _update():
    target = _download()
    _extract(target)
