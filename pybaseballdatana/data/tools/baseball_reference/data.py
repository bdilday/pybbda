import pandas as pd
import pathlib
import os
from ._update import _update_file
from . import WAR_PITCHING_URL, WAR_BATTING_URL

DATA_PATH = (
    pathlib.Path(__file__).absolute().parent.parent.parent
    / "assets"
    / "BaseballReference"
)
BASEBALL_REFERENCE_TABLES = {
    "war_bat": "war_daily_bat.txt",
    "war_pitch": "war_daily_pitch.txt",
}
BASEBALL_REFERENCE_URLS = {"war_bat": WAR_BATTING_URL, "war_pitch": WAR_PITCHING_URL}


class BaseballReferenceData:
    def __init__(self, data_path=DATA_PATH, update=False):
        self.tables = BASEBALL_REFERENCE_TABLES
        self.update = update
        self.data_path = data_path

    def _locate_file(self, name, update=False):
        data_file = self.tables[name]
        full_path = str(self.data_path / data_file)
        print("searching for file ", full_path)

        if os.path.exists(full_path):
            return full_path
        elif os.path.exists(full_path + ".gz"):
            return full_path + ".gz"
        elif update:
            print("updating file ", full_path)
            _update_file(BASEBALL_REFERENCE_URLS[name])
            return self._locate_file(name, False)
        else:
            raise FileNotFoundError(f"Cannot find file {full_path}")

    def _load(self, name):
        file_full_path = self._locate_file(name, self.update)
        return pd.read_csv(file_full_path)

    def __getattr__(self, name):
        if name not in self.tables.keys():
            raise AttributeError
        try:
            self.__dict__[name] = self._load(name)
            return self.__dict__[name]
        except FileNotFoundError:
            raise AttributeError
