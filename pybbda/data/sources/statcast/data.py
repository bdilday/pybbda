import logging
import datetime

import pandas as pd

from .constants import STATCAST_PBP_URL_FORMAT
from pybbda import PYBBDA_DATA_ROOT
from pybbda.data.sources.data_source.base import DataSource

STATCAST_DATA_PATH = PYBBDA_DATA_ROOT / "statcast"

STATCAST_TABLES = {}

STATCAST_URLS = {"statcast_daily": STATCAST_PBP_URL_FORMAT}

logger = logging.getLogger(__name__)


class StatcastData(DataSource):
    _SOURCE_DATA_PATH = STATCAST_DATA_PATH
    _SOURCE_TABLES = STATCAST_TABLES
    _SOURCE_URLS = STATCAST_URLS

    def get_statcast_daily(self, player_type, start_date, end_date, player_id=""):
        """

        :param player_type:
        :param start_date:
        :param end_date:
        :return:
        """
        self._validate_dates(start_date, end_date)

        if player_type == "pitcher":
            player_id_var = "pitchers_lookup%5B%5D"
        elif player_type == "batter":
            player_id_var = "batters_lookup%5B%5D"
        else:
            raise ValueError(f"player_type must be (pitcher, batter) not {player_type}")
        url = STATCAST_PBP_URL_FORMAT.format(
            **{
                "player_id_var": player_id_var,
                "player_id": player_id,
                "player_type": player_type,
                "season": start_date[0:4],
                "start_date": start_date,
                "end_date": end_date,
            }
        )

        print(url)
        daily_df = pd.read_csv(url)
        if len(daily_df) == 40000:
            logger.warning(
                "Statcast query returned 40000 rows which probably "
                "means you've exceeded the data limit. "
                "You should try to break up the query."
            )

        return self._format_daily_df(daily_df)

    def _format_daily_df(self, daily_df):
        # TODO: convert columns
        return daily_df

    def _validate_dates(self, start_date, end_date):
        if start_date > end_date:
            raise ValueError(
                f"start_date ({start_date}) cannot be "
                f"greater than end_date ({end_date})"
            )
        start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        dt_days = (end_dt - start_dt).days
        if dt_days >= 7:
            logger.warning(
                "end_date is greater than 6 days ahead of start date (%d days). "
                "This is likely to cause the query to exceed data limits of the API.",
                dt_days,
            )
