from io import BytesIO
import os
import requests
import zipfile
import glob
import pathlib
import re

from tqdm import tqdm
import logging
from pybaseballdatana.data.sources.retrosheet.data import RetrosheetData

logger = logging.getLogger(__name__)

RETROSHEET_URL = "https://github.com/chadwickbureau/retrosheet/archive/master.zip"


def _download(output_root):
    target = os.path.join(output_root, "retrosheet")
    archive_path = os.path.join(target, "retrosheet-master")
    if os.path.exists(archive_path):
        logger.info("path %s exists, not downloading", archive_path)
    else:
        logger.info("downloading file from %s", RETROSHEET_URL)
        archive = zipfile.ZipFile(
            BytesIO(requests.get(RETROSHEET_URL, stream=True).content)
        )
        archive.extractall(path=target)
    return archive_path


def _validate_path(output_root):
    output_root = output_root or pathlib.Path(__file__).parent.parent / "assets"
    if not os.path.exists(output_root):
        raise ValueError(f"Path {output_root} does not exist")
    if not os.path.isdir(output_root):
        raise ValueError(f"Path {output_root} must be a directory")


def _filter_event_files(event_files, min_year, max_year):
    result = []
    for event_file in event_files:
        year = int(re.search("^([0-9]{4})", os.path.basename(event_file)).group(1))
        if min_year <= year <= max_year:
            logger.debug("including file %s", event_file)
            result.append(event_file)

    return result


def _create_database(retrosheet_data, event_files):
    logger.info(f"creating database with {len(event_files)} files")

    retrosheet_data.create_database()
    retrosheet_data.initialize_table(retrosheet_data.df_from_file(event_files[0]))
    for event_file in tqdm(event_files[1:]):
        retrosheet_data.update_table(retrosheet_data.df_from_file(event_file))


def _update(output_root=None, min_year=1871, max_year=2019, create_database=False):
    output_root = output_root or pathlib.Path(__file__).parent.parent / "assets"
    _validate_path(output_root)
    retrosheet_data = RetrosheetData(output_root)
    target = _download(output_root)
    event_files = _filter_event_files(
        glob.glob(os.path.join(target, "event", "regular", "*EV*")), min_year, max_year
    )

    if create_database:
        _create_database(retrosheet_data, event_files)
