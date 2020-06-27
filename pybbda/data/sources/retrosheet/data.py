import os
import psycopg2
import pandas as pd
import logging
import glob

from sqlalchemy import create_engine
from pychadwick.chadwick import Chadwick
from pybbda import PYBBDA_DATA_ROOT
from pybbda.data.sources.data_source.base import DataSource

RETROSHEET_DATA_PATH = PYBBDA_DATA_ROOT / "retrosheet"
RETROSHEET_TABLES = {"people": "people.csv"}
RETROSHEET_URLS = {
    "people": "https://raw.githubusercontent.com/"
    "chadwickbureau/"
    "register/"
    "master/"
    "data/"
    "people.csv"
}

logger = logging.getLogger(__name__)


class RetrosheetData(DataSource):
    _SOURCE_DATA_PATH = RETROSHEET_DATA_PATH
    _SOURCE_TABLES = RETROSHEET_TABLES
    _SOURCE_URLS = RETROSHEET_URLS

    def __init__(self, data_root=None):
        super().__init__()
        self.data_root = data_root or PYBBDA_DATA_ROOT
        self.db_dir = os.path.join(self.data_root, "retrosheet")
        self.db_path = os.path.join(self.db_dir, "retrosheet.db")
        self._engine = None
        self.chadwick = Chadwick()

    def _connect_to_postgres(self, database="retrosheet"):
        conn = psycopg2.connect(
            database=database,
            user=os.environ["PSQL_USER"],
            password=os.environ["PSQL_PASS"],
            port=os.environ["PSQL_PORT"],
        )
        return conn

    def create_database(self):
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir, exist_ok=True)
        self._engine = create_engine(f"sqlite:///{self.db_path}", echo=False)

    @property
    def event_files(self):
        return sorted(
            glob.glob(
                os.path.join(
                    self.data_root,
                    "retrosheet",
                    "retrosheet-master",
                    "event",
                    "regular",
                    "*EV*",
                )
            )
        )

    @property
    def engine(self):
        if not self._engine:
            self._engine = create_engine(f"sqlite:///{self.db_path}", echo=False)
        return self._engine

    def initialize_table(self, df, conn=None):
        conn = conn or self.engine
        df.to_sql("event", conn, index=False, if_exists="replace")

    def update_table(self, df, conn=None):
        logger.debug("updating table with %s", df.GAME_ID.iloc[0])
        conn = conn or self.engine
        df.to_sql("event", conn, index=False, if_exists="append")

    def query(self, query):
        return pd.read_sql_query(query, self.engine)

    def df_from_team_id(self, team_id):
        for suffix in ["EVA", "EVN"]:
            event_file = os.path.join(
                self.db_dir,
                "retrosheet-master",
                "event",
                "regular",
                f"{team_id}.{suffix}",
            )
            if os.path.exists(event_file):
                logger.debug("loading events from %s", event_file)
                return self.df_from_file(event_file)

        found_remote_file = False
        for suffix in ["EVA", "EVN"]:
            event_url = os.path.join(
                "https://raw.githubusercontent.com/"
                "chadwickbureau/"
                "retrosheet/"
                "master/"
                "event/"
                "regular",
                f"{team_id}.{suffix}",
            )
            logger.debug("loading event from URL %s", event_url)
            try:
                remote_df = self.df_from_file(event_url)
                found_remote_file = True
                return remote_df
            except ValueError:
                logger.debug(f"cannot find remote file {event_url}")

        if not found_remote_file:
            raise FileNotFoundError(f"cannot locate team_id {team_id}")

    def df_from_file(self, file_path):
        games = self.chadwick.games(file_path)
        return self.chadwick.games_to_dataframe(games)
