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
    
    archive = zipfile.ZipFile(BytesIO(requests.get(LAHMAN_URL, stream=True).content))
    target = tempfile.gettempdir()
    archive.extractall(path=target)
    return target


def _extract(target):
    output_path = pathlib.Path(__file__).parent / "BaseballReference"
    extracted_files = glob.glob(os.path.join(target, "**", "*csv"), recursive=True)
    for extracted_file in extracted_files:
        shutil.copy(extracted_file, output_path)


def _update():
    for url in [WAR_BATTING_URL, WAR_PITCHING_URL]:
    target = _download()
    _extract(target)
