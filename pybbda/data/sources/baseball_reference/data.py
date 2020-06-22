import pandas as pd
import os
from . import WAR_PITCHING_URL, WAR_BATTING_URL
from pybbda import PYBBDA_DATA_ROOT
import logging

BBREF_DATA_PATH = PYBBDA_DATA_ROOT / "BaseballReference"

BASEBALL_REFERENCE_TABLES = {
    "war_bat": "war_daily_bat.txt",
    "war_pitch": "war_daily_pitch.txt",
}
BASEBALL_REFERENCE_URLS = {"war_bat": WAR_BATTING_URL, "war_pitch": WAR_PITCHING_URL}

logger = logging.getLogger(__name__)


class BaseballReferenceData:
    def __init__(self, data_path=None):
        if data_path is None:
            data_path = BBREF_DATA_PATH
        self.tables = BASEBALL_REFERENCE_TABLES
        self.data_path = data_path

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
