import argparse
import os
import sys
import logging
import pathlib
from pybaseballdatana import PYBBDA_DATA_ROOT, PYBBDA_LOG_LEVEL

from ..sources.lahman._update import _update as update_lahman
from ..sources.baseball_reference._update import _update as update_bbref
from ..sources.fangraphs._update import _update as update_fangraphs

logger = logging.getLogger(__name__)
logger.setLevel(PYBBDA_LOG_LEVEL)

DATA_SOURCE_OPTIONS = ["Lahman", "BaseballReference", "Fangraphs"]

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
    return parser.parse_args(sys.argv[1:])


def update_source(data_root, data_source):
    if data_source == "Lahman":
        update_lahman(data_root)
    elif data_source == "BaseballReference":
        update_bbref(data_root)
    elif data_source=="Fangraphs":
        update_fangraphs(data_root)
    else:
        raise ValueError(data_source)


def create_dir_if_not_exist(data_root):
    os.makedirs(data_root, exist_ok=True)


def main():
    args = _parse_args()

    if args.make_dirs:
        create_dir_if_not_exist(args.data_root)

    if not os.path.exists(args.data_root):
        logging.critical("The target path %s does not exist. You can create it or pass option --make-dirs to update to create it automatically", args.data_root)
        raise ValueError(f"missing target path {args.data_root}. You can create it or pass option --make-dirs to update to create it automatically")

    data_sources = DATA_SOURCE_OPTIONS if args.data_source == "all" else [args.data_source]
    for data_source in data_sources:
        update_source(args.data_root, data_source)


if __name__ == "__main__":
    main()
