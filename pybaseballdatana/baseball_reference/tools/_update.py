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


WAR_BATTING_URL = "https://www.baseball-reference.com/data/war_daily_bat.txt"
WAR_PITCHING_URL = "https://www.baseball-reference.com/data/war_daily_pitch.txt"


def _download_csv(url):
    logging.info("downloading file from {}".format(url))
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        logging.info("there was a download error code={}", response.status_code)
        raise FileNotFoundError
    it = response.iter_lines()
    return list(it)


def _extract(lines, file_name):
    output_path = (
        pathlib.Path(__file__).absolute().parent.parent.parent
        / "assets"
        / "BaseballReference"
        / file_name
    )
    logging.info("saving file to {}".format(output_path))
    with open(output_path, "w") as fh:
        csvw = csv.writer(fh)
        csvw.writerows(lines)


def _update():
    for url in [WAR_BATTING_URL, WAR_PITCHING_URL]:
        lines = _download_csv(url)
        _extract(lines, os.path.basename(url))
