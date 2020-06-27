import logging

from .constants import FANGRAPHS_GUTS_CONSTANTS_URL
from pybbda import PYBBDA_DATA_ROOT
from pybbda.data.sources.data_source.base import DataSource

FANGRAPHS_DATA_PATH = PYBBDA_DATA_ROOT / "Fangraphs"

FANGRAPHS_TABLES = {"fg_guts_constants": "fg_guts_constants.csv"}
FANGRAPHS_TABLES.update(
    {f"fg_batting_{season}": f"fg_bat_{season}.csv" for season in range(1871, 2020)}
)

FANGRAPHS_TABLES.update(
    {f"fg_pitching_{season}": f"fg_pit_{season}.csv" for season in range(1871, 2020)}
)

FANGRAPHS_TABLES.update(
    {
        f"fg_park_factors_{season}": f"fg_park_factors_{season}.csv"
        for season in range(1871, 2020 - 1)
    }
)
FANGRAPHS_TABLES.update(
    {
        f"fg_park_factors_handedness_{season}": f"fg_park_factors_handedness_{season}.csv"
        for season in range(2002, 2020 - 1)
    }
)

FANGRAPHS_URLS = {"fg_guts_constants": FANGRAPHS_GUTS_CONSTANTS_URL}

logger = logging.getLogger(__name__)


class FangraphsData(DataSource):
    _SOURCE_DATA_PATH = FANGRAPHS_DATA_PATH
    _SOURCE_TABLES = FANGRAPHS_TABLES
    _SOURCE_URLS = FANGRAPHS_URLS
