import pathlib
import re
import os

import pandas as pd

from ..lahman import _LAHMAN_TABLES
from pybaseballdatana import PYBBDA_DATA_ROOT

LAHMAN_DATA_PATH = PYBBDA_DATA_ROOT / "Lahman"


class LahmanData:
    def __init__(self, data_path=LAHMAN_DATA_PATH):
        self.data_path = data_path
        for file_name in _LAHMAN_TABLES:
            self.__setattr__(self._munge_attr_name(file_name), None)

    @staticmethod
    def _munge_attr_name(name):
        patts = [r"(^[a-z]{1})", r"_+([a-zA-Z]{1})"]
        for patt in patts:
            name = re.sub(patt, lambda m: m.group(1).upper(), name)
        name = name.replace("_", "")
        return name

    def _load(self, name):
        updated_name = self._munge_attr_name(name)
        data_file = updated_name + ".csv"
        full_path = str(self.data_path / data_file)
        print("searching for file ", full_path)
        if os.path.exists(full_path):
            return pd.read_csv(full_path)
        elif os.path.exists(full_path + ".gz"):
            return pd.read_csv(full_path + ".gz")
        else:
            raise FileNotFoundError(f"Cannot find file {full_path}")

    def __getattr__(self, name):
        if self._munge_attr_name(name) not in _LAHMAN_TABLES:
            raise AttributeError
        try:
            self.__dict__[name] = self.__dict__.get(name, self._load(name))
            return self.__dict__[name]
        except FileNotFoundError:
            raise AttributeError
