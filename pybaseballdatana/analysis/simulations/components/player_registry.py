from pybaseballdatana.data import LahmanData
from pybaseballdatana.data.tools.lahman.data import augment_lahman_batting
from pybaseballdatana.utils import Singleton

from .player import Batter, BattingEventProbability


class PlayerRegistry(Singleton):
    def __init__(self):
        self.registry = {}

    def _add_one(self, batter):
        self.registry[batter.player_id] = batter

    def add(self, batters):
        if not isinstance(batters, list):
            batters = [batters]
        for batter in batters:
            self._add_one(batter)
        return self.registry

    @property
    def len(self):
        return len(self.registry)

    def _get_lahman_records(self, pa_limit):
        batting_df = (
            augment_lahman_batting(LahmanData().batting)
            .groupby(["playerID", "yearID"])
            .sum()
            .query(f"PA >= {pa_limit}")
        )

        probability_columns = (
            "base_on_balls",
            "single",
            "double",
            "triple",
            "home_run",
        )
        stat_columns = ("BB", "1B", "2B", "3B", "HR")
        for probability_column, stat_column in zip(probability_columns, stat_columns):
            batting_df.loc[:, probability_column] = (
                batting_df.loc[:, stat_column] / batting_df.loc[:, "PA"]
            )
        return (
            (
                batting_df.reset_index()
                .assign(
                    player_id=lambda row: row.playerID + "_" + row.yearID.astype("str")
                )
                .loc[:, ["player_id"] + list(probability_columns)]
            )
            .set_index("player_id")
            .to_dict(orient="index")
        )

    def load_from_lahman(self, pa_limit=180):
        lahman_records = self._get_lahman_records(pa_limit=pa_limit)
        for player_id, record in lahman_records.items():
            self.add(
                Batter(
                    player_id=player_id,
                    batting_event_probabilities=BattingEventProbability(**record),
                )
            )
