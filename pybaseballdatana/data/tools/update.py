import argparse
import os
import sys
import logging

from pybaseballdatana import PYBBDA_DATA_ROOT, PYBBDA_LOG_LEVEL
from pybaseballdatana.data.sources.lahman._update import _update as update_lahman
from pybaseballdatana.data.sources.baseball_reference._update import (
    _update as update_bbref,
)
from pybaseballdatana.data.sources.fangraphs._update import _update as update_fangraphs
from pybaseballdatana.data.sources.retrosheet._update import (
    _update as update_retrosheet,
)

logger = logging.getLogger(__name__)
logger.setLevel(PYBBDA_LOG_LEVEL)

DATA_SOURCE_OPTIONS = ["Lahman", "BaseballReference", "Fangraphs", "retrosheet"]
NUM_THREADS = 1


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-root",
        required=False,
        default=PYBBDA_DATA_ROOT,
        help="Root directory for data storage",
    )
    parser.add_argument(
        "--data-source",
        required=True,
        choices=DATA_SOURCE_OPTIONS + ["all"],
        help="Update source",
    )
    parser.add_argument(
        "--make-dirs",
        required=False,
        action="store_true",
        help="Make root dir if does not exist",
    )
    parser.add_argument(
        "--overwrite",
        required=False,
        action="store_true",
        help="Overwrite files if they exist",
    )
    parser.add_argument(
        "--create-event-database",
        required=False,
        action="store_true",
        help="Create a sqlite database for retrosheet event files",
    )
    parser.add_argument(
        "--min-year",
        required=False,
        type=int,
        default=2018,
        help="Min year to download",
    )
    parser.add_argument(
        "--max-year",
        required=False,
        type=int,
        default=2019,
        help="Max year to download",
    )
    parser.add_argument(
        "--num-threads",
        required=False,
        type=int,
        default=NUM_THREADS,
        help="Number of threads to use for downloads",
    )

    return parser.parse_args(sys.argv[1:])


def update_source(
    data_root, data_source, min_year, max_year, num_threads, overwrite, create_database
):
    if data_source == "Lahman":
        update_lahman(data_root)
    elif data_source == "BaseballReference":
        update_bbref(data_root)
    elif data_source == "Fangraphs":
        update_fangraphs(
            data_root,
            min_year=min_year,
            max_year=max_year,
            num_threads=num_threads,
            overwrite=overwrite,
        )
    elif data_source == "retrosheet":
        update_retrosheet(
            data_root,
            min_year=min_year,
            max_year=max_year,
            create_database=create_database,
        )
    else:
        raise ValueError(data_source)


def create_dir_if_not_exist(data_root):
    os.makedirs(data_root, exist_ok=True)


def main():
    args = _parse_args()

    if args.make_dirs:
        create_dir_if_not_exist(args.data_root)

    if not os.path.exists(args.data_root):
        raise ValueError(
            f"missing target path {args.data_root}. "
            f"You can create it or pass option --make-dirs "
            f"to update to create it automatically"
        )

    data_sources = (
        DATA_SOURCE_OPTIONS if args.data_source == "all" else [args.data_source]
    )

    for data_source in data_sources:
        update_source(
            args.data_root,
            data_source,
            args.min_year,
            args.max_year,
            args.num_threads,
            args.overwrite,
            args.create_event_database,
        )


if __name__ == "__main__":
    main()
