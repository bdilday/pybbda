import os

import logging

import pandas as pd
from pybbda.utils import Singleton

logger = logging.getLogger(__name__)


class DataSource(Singleton):
    _SOURCE_DATA_PATH = None
    _SOURCE_TABLES = None
    _SOURCE_URLS = None

    def __init__(self, data_path=None):
        self.tables = self._SOURCE_TABLES
        self.data_path = data_path or self._SOURCE_DATA_PATH

    def _locate_file(self, name):
        data_file = self.tables[name]
        full_path = str(self.data_path / data_file)
        logger.info("searching for file %s", full_path)

        if os.path.exists(full_path):
            return full_path
        elif os.path.exists(full_path + ".gz"):
            return full_path + ".gz"
        else:
            raise FileNotFoundError(f"Cannot find file {full_path}")

    def _load(self, name):
        file_full_path = self._locate_file(name)
        return pd.read_csv(file_full_path)

    def __getattr__(self, name):
        if name not in self.tables.keys():
            raise AttributeError
        try:
            self.__dict__[name] = self._load(name)
            return self.__dict__[name]
        except FileNotFoundError:
            raise AttributeError
