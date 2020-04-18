import os
import requests
import pathlib
import logging
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


def _save(lines, file_name, output_path=None):
    output_path = (output_path or
        pathlib.Path(__file__).absolute().parent.parent
        / "assets"
        / "BaseballReference"
    )
    output_file_path = os.path.join(output_path, file_name)
    output_payload = "\n".join(str(line, "utf-8") for line in lines)
    logging.info("saving file to {}".format(output_file_path))
    with gzip.open(output_file_path, "wb") as fh:
        fh.write(bytes(output_payload, encoding="utf-8"))


def _update_file(url, output_path=None):
    lines = _download_csv(url)
    _save(lines, os.path.basename(url) + ".gz", output_path)


def _update(output_path=None):
    for url in [WAR_BATTING_URL, WAR_PITCHING_URL]:
        _update_file(url, output_path)
