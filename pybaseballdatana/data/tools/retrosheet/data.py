import os
import psycopg2
import pandas as pd
import logging


class RetrosheetData:
    def __init__(self, database="retrosheet"):
        self.conn = psycopg2.connect(
            database=database,
            user=os.environ["PSQL_USER"],
            password=os.environ["PSQL_PASS"],
            port=os.environ["PSQL_PORT"],
        )
        self._event = None

    def query(self, query):
        return pd.read_sql_query(query, self.conn)

    # @property
    # def event(self):
    #     if self._event is None:
    #         logging.info("loading event data from sql")
    #         self._event = pd.read_sql_query("select * from event", self.conn)
    #     return self._event
