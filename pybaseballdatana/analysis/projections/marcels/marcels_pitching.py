import pandas as pd
import numpy as np
from pybaseballdatana.data.tools.processing.aggregate import aggregate_by_season
from pybaseballdatana.data.tools.processing.transform import get_age
from pybaseballdatana.data.tools.lahman.data import augment_lahman_pitching
from pybaseballdatana.data import LahmanData
import sys
from pybaseballdatana.analysis.projections.marcels.age_adjustment import age_adjustment
from pybaseballdatana.analysis.projections.marcels.marcels_base import (
    MarcelsProjectionsBase,
)

# http://www.tangotiger.net/archives/stud0346.shtml
import logging


class MarcelProjectionsPitching(MarcelsProjectionsBase):
    COMPUTED_METRICS = ["H", "HR", "ER", "BB", "SO", "HBP", "R"]
    RECIPROCAL_AGE_METRICS = ["H", "HR", "ER", "BB", "HBP", "R"]
    LEAGUE_AVG_PT = 134
    METRIC_WEIGHTS = (3, 2, 1)
    PT_WEIGHTS = (0.5, 0.1, 0)
    REQUIRED_COLUMNS = ["IPouts"]

    def __init__(self, stats_df=None, primary_pos_df=None):
        super().__init__(stats_df, primary_pos_df)

    def _load_data(self):
        return self.ld.pitching

    def preprocess_data(self, stats_df):
        return aggregate_by_season(augment_lahman_pitching(stats_df))

    def remove_non_pitchers(self, stats_df, primary_pos_df):
        return (
            stats_df.merge(primary_pos_df, on=["playerID", "yearID"], how="left")
            .query(r'primaryPos == "P"')
            .drop("primaryPos", axis=1)
        )

    def metric_projection(self, metric_name, projected_season):
        x_df = self.metric_projection_detail(metric_name, projected_season)
        return (
            x_df.assign(
                x=lambda row: row.rate_projection
                * row.pt_projection
                * row.age_adjustment_value
            )
            .rename({"x": metric_name}, axis=1)
            .loc[:, [metric_name]]
        )

    def metric_projection_detail(self, metric_name, projected_season):
        season = projected_season - 1

        seasonal_avg_df = (
            self.seasonal_average(
                self.remove_non_pitchers(self.stats_df, self.primary_pos_df),
                metric_name,
                playing_time_column="IPouts",
            )
            .reset_index()
            .loc[:, ["yearID", "seasonal_avg"]]
        )

        stats_df = self.stats_df.loc[:, ["playerID", "yearID", "IPouts", metric_name]]
        stats_df_season = stats_df.query(f"yearID == {season}").loc[
            :, ["playerID", "yearID"]
        ]

        fraction_games_started = (
            self.stats_df.query(f"yearID == {season}")
            .apply(lambda row: row["GS"] / row["G"], axis=1)
            .values
        )

        metric_df = pd.concat(
            [
                (
                    stats_df_season.merge(
                        stats_df.assign(
                            yearID=lambda row: row.yearID + prior_year_offset
                        ),
                        on=["playerID", "yearID"],
                        how="left",
                        suffixes=["_x", ""],
                    )
                    .set_index(["playerID", "yearID"])
                    .loc[:, metric_name]
                )
                for prior_year_offset, _ in enumerate(self.metric_weights)
            ],
            axis=1,
        ).fillna(0)

        pt_df = pd.concat(
            [
                (
                    stats_df_season.merge(
                        stats_df.assign(
                            yearID=lambda row: row.yearID + prior_year_offset
                        ),
                        on=["playerID", "yearID"],
                        how="left",
                        suffixes=["_x", ""],
                    )
                    .set_index(["playerID", "yearID"])
                    .loc[:, "IPouts"]
                )
                for prior_year_offset, _ in enumerate(self.metric_weights)
            ],
            axis=1,
        ).fillna(0)

        sa_df = seasonal_avg_df.query(
            f"yearID >= {season - len(self.metric_weights)+1} and yearID <= {season}"
        ).loc[:, "seasonal_avg"]

        rate_projection = self.compute_rate_projection(
            metric_df.values,
            pt_df.values,
            self.metric_weights,
            self.pt_weights,
            sa_df.values,
        )

        pt_projection = self.compute_playing_time_projection(
            metric_df.values,
            pt_df.values,
            self.metric_weights,
            self.pt_weights,
            sa_df.values,
            num_regression_pt=75 + 105 * fraction_games_started,
        )

        age_df = get_age(stats_df_season, self.people)
        age_values = age_df.age + 1
        age_adjustment_value = age_values.apply(age_adjustment).values

        if metric_name in self.RECIPROCAL_AGE_METRICS:
            age_adjustment_value = 1 / age_adjustment_value

        return stats_df_season.assign(
            yearID=projected_season,
            rate_projection=rate_projection,
            pt_projection=pt_projection,
            age_adjustment_value=age_adjustment_value,
        ).set_index(["playerID", "yearID"])

    def compute_rate_projection(
        self,
        metric_values,
        pt_values,
        metric_weights,
        pt_weights,
        seasonal_averages,
        num_regression_pt=134,
    ):
        pt_values[pt_values == 0] = sys.float_info.min
        normalized_metric_weights = np.array(metric_weights) / sum(metric_weights)
        unregressed_player_projection = np.sum(
            metric_values * normalized_metric_weights, 1
        )

        mean_rate_projection = np.sum(
            seasonal_averages * pt_values * normalized_metric_weights, 1
        ) / np.sum(pt_values * normalized_metric_weights, 1)

        projection_numerator = (
            unregressed_player_projection + num_regression_pt * mean_rate_projection
        )
        projection_denominator = (
            np.sum(pt_values * normalized_metric_weights, 1) + num_regression_pt
        )

        return projection_numerator / projection_denominator

    def compute_playing_time_projection(
        self,
        metric_values,
        pt_values,
        metric_weights,
        pt_weights,
        seasonal_averages,
        num_regression_pt,
    ):

        #        75 + data$GS/data$G * 105

        return np.sum(pt_values * pt_weights, 1) + num_regression_pt


if __name__ == "__main__":

    ld = LahmanData()

    md = MarcelProjectionsPitching(ld.pitching)

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
    print(res.sort_values("SO", ascending=False))
    print(dt, dt / cnt)
