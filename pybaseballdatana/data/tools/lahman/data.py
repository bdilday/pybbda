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


def get_primary_position(fielding_df):
    fld_combined_stints = (
        fielding_df.groupby(["playerID", "yearID", "POS"]).sum().reset_index()
    )
    gm_rank_df = (
        fld_combined_stints.groupby(["playerID", "yearID"])
        .G.rank(method="first", ascending=False)
        .to_frame()
        .rename({"G": "gm_rank"}, axis=1)
    )
    return (
        pd.concat((fld_combined_stints, gm_rank_df), axis=1)
        .query("gm_rank == 1")
        .drop("gm_rank", axis=1)
        .filter(["playerID", "yearID", "POS"])
        .rename({"POS": "primaryPos"}, axis=1)
    )


def compute_pa(bat_df):
    PA = bat_df.loc[:, "AB"].fillna(0)
    for stat in ["BB", "HBP", "SH", "SF"]:
        PA += bat_df.loc[:, stat].fillna(0)
    return PA.astype(int)


def augment_lahman_batting(bat_df):
    PA = bat_df.loc[:, "AB"].fillna(0)
    for stat in ["BB", "HBP", "SH", "SF"]:
        PA += bat_df.loc[:, stat].fillna(0)
    X1B = (
        bat_df.loc[:, "H"]
        - bat_df.loc[:, "2B"]
        - bat_df.loc[:, "3B"]
        - bat_df.loc[:, "HR"]
    )
    TB = (
        bat_df.loc[:, "HR"] * 4
        + bat_df.loc[:, "3B"] * 3
        + bat_df.loc[:, "2B"] * 2
        + X1B
    )
    return bat_df.assign(
        PA=PA.astype(int), X1B=X1B.astype(int), TB=TB.astype(int)
    ).rename({"X1B": "1B"}, axis=1)

def augment_lahman_pitching(stats_df):
    return stats_df
