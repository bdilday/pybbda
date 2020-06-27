"""
pybbda data module

some data, and blah
"""

from pandas import Int32Dtype

from pybbda.data.sources.lahman.data import LahmanData
from pybbda.data.sources.baseball_reference.data import BaseballReferenceData
from pybbda.data.sources.retrosheet.data import RetrosheetData
from pybbda.data.sources.fangraphs.data import FangraphsData
from pybbda.data.sources.statcast.data import StatcastData

nullable_int = Int32Dtype()

__all__ = [
    "LahmanData",
    "BaseballReferenceData",
    "RetrosheetData",
    "FangraphsData",
    "StatcastData",
]
