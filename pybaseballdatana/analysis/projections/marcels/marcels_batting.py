from pybaseballdatana.data.tools.processing.aggregate import aggregate_by_season
from pybaseballdatana.data.tools.lahman.data import augment_lahman_batting
from pybaseballdatana.data import LahmanData
from pybaseballdatana.analysis.projections.marcels.marcels_base import (
    MarcelsProjectionsBase,
)


class MarcelProjectionsBatting(MarcelsProjectionsBase):
    COMPUTED_METRICS = [
        "1B",
        "2B",
        "3B",
        "HR",
        "BB",
        "HBP",
        "SB",
        "CS",
        "SO",
        "SH",
        "SF",
    ]
    RECIPROCAL_AGE_METRICS = ["SO", "CS"]
    LEAGUE_AVG_PT = 100
    NUM_REGRESSION_PLAYING_TIME = 200
    METRIC_WEIGHTS = (5, 4, 3)
    PT_WEIGHTS = (0.5, 0.1, 0)
    REQUIRED_COLUMNS = ["AB", "BB"]
    PLAYING_TIME_COLUMN = "PA"

    def __init__(self, stats_df=None, primary_pos_df=None):
        super().__init__(stats_df, primary_pos_df)

    def _load_data(self):
        return self.ld.batting

    def preprocess_data(self, stats_df):
        return aggregate_by_season(augment_lahman_batting(stats_df))

    def filter_non_representative_data(self, stats_df, primary_pos_df):
        return (
            stats_df.merge(primary_pos_df, on=["playerID", "yearID"], how="left")
            .query(r'primaryPos != "P"')
            .drop("primaryPos", axis=1)
        )


if __name__ == "__main__":

    ld = LahmanData()

    md = MarcelProjectionsBatting(ld.batting)

    import time

    start = time.time()
    cnt = 0
    for season in range(2019, 2020 + 1):
        cnt += 1
        res = md.projections(season)
        # print(res)
        # print(res[res.playerID.str.contains("^bel")])
    end = time.time()
    dt = end - start
    print(res.sort_values("HR", ascending=False))
    print(dt, dt / cnt)
