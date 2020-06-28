import os
import requests
import pathlib
import logging
import gzip
import itertools
from functools import partial
import multiprocessing

from .constants import (
    FANGRAPHS_GUTS_CONSTANTS_URL,
    FANGRAPHS_PARK_FACTORS_FORMAT,
    FANGRAPHS_PARK_FACTORS_HANDEDNESS_FORMAT,
    FANGRAPHS_LEADERBOARD_DEFAULT_CONFIG,
    FANGRAPHS_LEADERBOARD_URL_FORMAT,
)
from pybbda.utils.html_table import url_to_table_rows

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


def _update_file(
    url,
    output_root,
    output_filename=None,
    table_id=None,
    rows_filter=None,
    overwrite=False,
):
    output_filename = output_filename or ".".join((os.path.basename(url), "gz"))
    output_path = os.path.join(output_root, "Fangraphs")
    os.makedirs(output_path, exist_ok=True)

    output_file_path = os.path.join(output_path, output_filename)
    if os.path.exists(output_file_path):
        if not overwrite:
            logger.info("file %s exists, not overwriting", output_file_path)
            return
        else:
            logger.warning("file %s exists, but overwriting", output_file_path)

    lines = url_to_table_rows(url, table_id)
    if rows_filter is not None:
        lines = rows_filter(lines)

    _save(lines, output_filename, output_path)


def _validate_path(output_root):
    output_root = output_root or pathlib.Path(__file__).parent.parent.parent / "assets"
    if not os.path.exists(output_root):
        raise ValueError(f"Path {output_root} does not exist")
    if not os.path.isdir(output_root):
        raise ValueError(f"Path {output_root} must be a directory")


stat_columns = {
    "bat": ",".join([str(i) for i in range(2, 305)]),
    "pit": ",".join([str(i) for i in range(2, 322)]),
}


def _pool_park_factors_update(overwrite=False, season_root=None):
    season, output_root = season_root
    config = {"season": season}

    url = FANGRAPHS_PARK_FACTORS_FORMAT.format(**config)
    _update_file(
        url,
        output_root,
        f"fg_park_factors_{season}.csv.gz",
        "GutsBoard1_dg1_ctl00",
        overwrite=overwrite,
    )

    if season >= 2002:
        url = FANGRAPHS_PARK_FACTORS_HANDEDNESS_FORMAT.format(**config)
        _update_file(
            url,
            output_root,
            f"fg_park_factors_handedness_{season}.csv.gz",
            "GutsBoard1_dg1_ctl00",
            overwrite=overwrite,
        )
    else:
        logger.info(f"handedness park factors not available for pre-2002 seasons. "
                    f"skipping {season}")


def _pool_do_update(overwrite=False, season_stats=None):
    season, stats, output_root = season_stats
    config = {
        **FANGRAPHS_LEADERBOARD_DEFAULT_CONFIG,
        "season_start": season,
        "season_end": season,
        "stats": stats,
        "columns": stat_columns[stats],
    }
    logger.debug("config %s", config)
    url = FANGRAPHS_LEADERBOARD_URL_FORMAT.format(**config)
    _update_file(
        url,
        output_root,
        f"fg_{stats}_{season}.csv.gz",
        "LeaderBoard1_dg1_ctl00",
        rows_filter=lambda r: r[1:2] + r[3:],
        overwrite=overwrite,
    )


def _update(
    output_root=None, min_year=1871, max_year=2019, num_threads=2, overwrite=False
):
    output_root = (
        output_root or pathlib.Path(__file__).absolute().parent.parent / "assets"
    )
    logger.debug("output root is %s", output_root)
    _validate_path(output_root)
    _update_file(
        FANGRAPHS_GUTS_CONSTANTS_URL,
        output_root,
        "fg_guts_constants.csv.gz",
        "GutsBoard1_dg1_ctl00",
    )

    seasons = range(min_year, max_year + 1)
    stat_names = ["bat", "pit"]

    logger.debug("Starting downloads with %d threads", num_threads)

    season_root_it = itertools.product(seasons, [output_root])
    func = partial(_pool_park_factors_update, overwrite)
    with multiprocessing.Pool(num_threads) as mp:
        mp.map(func, season_root_it)

    season_stats_it = itertools.product(seasons, stat_names, [output_root])
    func = partial(_pool_do_update, overwrite)
    # TODO: consider using a concurrent.futures.ThreadPoolExecutor instead
    with multiprocessing.Pool(num_threads) as mp:
        mp.map(func, season_stats_it)
