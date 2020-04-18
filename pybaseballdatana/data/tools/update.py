import argparse
import os
import sys
import pathlib
from pybaseballdatana import PYBBDA_DATA_ROOT


from .lahman._update import _update as update_lahman
from .baseball_reference._update import _update as update_bbref

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
        choices=("Lahman", "BaseballReference"),
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
        update_lahman(os.path.join(data_root, data_source))
    elif data_source == "BaseballReference":
        update_bbref(os.path.join(data_root, data_source))


def create_dir_if_not_exist(data_root, data_source):
    os.makedirs(os.path.join(data_root, data_source), exist_ok=True)

def main():
    args = _parse_args()
    if args.make_dirs:
        create_dir_if_not_exist(args.data_root, args.data_source)
    update_source(args.data_root, args.data_source)

if __name__ == "__main__":
    main()
