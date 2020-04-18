import argparse
import os
import sys
import pathlib
from pybaseballdatana import PYBBDA_DATA_ROOT


from .lahman._update import _update as update_lahman


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-root",
        required=False,
        default=PYBBDA_DATA_ROOT,
        help="Root directory for data storage",
    )
    parser.add_argument(
        "--update-source",
        required=True,
        choices=("lahman", "baseball-reference"),
        help="Update source",
    )
    parser.add_argument(
        "--make-dirs",
        required=False,
        action="store_true",
        help="Make root dir if does not exist",
    )
    return parser.parse_args(sys.argv[1:])


def main():
    args = _parse_args()
    if args.make_dirs:
        os.makedirs(os.path.join(args.data_root, "Lahman"), exist_ok=True)
    update_lahman(os.path.join(args.data_root, "Lahman"))


if __name__ == "__main__":
    main()
