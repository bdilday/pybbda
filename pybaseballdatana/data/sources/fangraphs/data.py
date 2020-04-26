
import logging

from . import FANGRAPHS_GUTS_CONSTANTS_URL
from pybaseballdatana import PYBBDA_DATA_ROOT
from pybaseballdatana.data.sources.data_source.base import DataSource

FANGRAPHS_DATA_PATH = PYBBDA_DATA_ROOT / "Fangraphs"

FANGRAPHS_TABLES = {
    "fg_guts_constants": "fg_guts_constants.csv",
}
FANGRAPHS_URLS = {"fg_guts_constants": FANGRAPHS_GUTS_CONSTANTS_URL,}

logger = logging.getLogger(__name__)

class FangraphsData(DataSource):
    SOURCE_DATA_PATH = FANGRAPHS_DATA_PATH
    SOURCE_TABLES = FANGRAPHS_TABLES
    SOURCE_URLS = FANGRAPHS_URLS

