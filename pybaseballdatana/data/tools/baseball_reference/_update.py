from io import BytesIO
import os
import requests
import tempfile
import zipfile
import pandas as pd
import joblib
import glob
import pathlib
import shutil
import logging
import csv
import gzip

from . import WAR_BATTING_URL, WAR_PITCHING_URL

def _download_csv(url):
    logging.info("downloading file from {}".format(url))
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        logging.info("there was a download error code={}", response.status_code)
        raise FileNotFoundError
    it = response.iter_lines()
    return list(it)


def _save(lines, file_name):
    output_path = (
        pathlib.Path(__file__).absolute().parent.parent.parent
        / "assets"
        / "BaseballReference"
        / file_name
    )
    output_payload = "\n".join(str(line, "utf-8") for line in lines)
    logging.info("saving file to {}".format(output_path))
    with gzip.open(output_path, "wb") as fh:
        fh.write(bytes(output_payload, encoding="utf-8"))

def _update_file(url):
    lines = _download_csv(url)
    _save(lines, os.path.basename(url) + ".gz")

def _update():
    for url in [WAR_BATTING_URL, WAR_PITCHING_URL]:
        _update_file(url)
