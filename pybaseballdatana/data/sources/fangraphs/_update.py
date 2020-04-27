import os
import requests
import pathlib
import logging
import gzip

from . import FANGRAPHS_GUTS_CONSTANTS_URL
from pybaseballdatana.utils.html_table import url_to_table_rows

logger = logging.getLogger(__name__)


def _download_csv(url):
    logger.info("downloading file from {}".format(url))
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        logger.info("there was a download error code={}", response.status_code)
        raise FileNotFoundError
    it = response.iter_lines()
    return list(it)


def _save(lines, file_name, output_path):
    output_file_path = os.path.join(output_path, file_name)
    output_payload = "\n".join(",".join(line) for line in lines)
    logger.info("saving file to {}".format(output_file_path))
    with gzip.open(output_file_path, "wb") as fh:
        fh.write(bytes(output_payload, encoding="utf-8"))


def _update_file(url, output_root, output_filename=None):
    output_filename = output_filename or ".".join(os.path.basename(url), "gz")
    output_path = os.path.join(output_root, "Fangraphs")
    os.makedirs(output_path, exist_ok=True)
    lines = url_to_table_rows(url, "GutsBoard1_dg1_ctl00")
    _save(lines, output_filename, output_path)


def _validate_path(output_root):
    output_root = output_root or pathlib.Path(__file__).parent.parent.parent / "assets"
    if not os.path.exists(output_root):
        raise ValueError(f"Path {output_root} does not exist")
    if not os.path.isdir(output_root):
        raise ValueError(f"Path {output_root} must be a directory")


def _update(output_root=None):
    output_root = (
        output_root or pathlib.Path(__file__).absolute().parent.parent / "assets"
    )
    logger.debug("output root is %s", output_root)
    _validate_path(output_root)
    _update_file(FANGRAPHS_GUTS_CONSTANTS_URL, output_root, "fg_guts_constants.csv.gz")
