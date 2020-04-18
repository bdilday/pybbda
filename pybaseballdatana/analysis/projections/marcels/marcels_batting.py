import pandas as pd
import numpy as np
from pybaseballdatana.data.tools.processing.aggregate import aggregate_batters_by_season
from pybaseballdatana.data.tools.processing.transform import get_age
from pybaseballdatana.data.tools.lahman.data import (
    get_primary_position,
    augment_lahman_batting,
)
from pybaseballdatana.data import LahmanData
import sys
from pybaseballdatana.analysis.projections.marcels.age_adjustment import age_adjustment

import numpy as np

# http://www.tangotiger.net/archives/stud0346.shtml


class MarcelProjectionsBatting:
    COMPUTED_METRICS = ["1B", "2B", "3B", "HR", "SB", "CS", "SO"]
    RECIPROCAL_AGE_METRICS = ["SO", "CS"]

    def __init__(self, bat_df=None, primary_pos_df=None):
        self.ld = LahmanData()

        self.bat_df = bat_df if bat_df is not None else self.ld.batting
        self.bat_df = self.preprocess_data(self.bat_df)
        self.primary_pos_df = (
            get_primary_position(self.ld.fielding)
            if primary_pos_df is None
            else primary_pos_df
        )
        self.metric_weights = np.array((5, 4, 3))
        self.pa_weights = np.array((0.5, 0.1, 0))
        self.league_avg_pa = 100
        self.people = self.ld.people

    def preprocess_data(self, stats_df):
        return aggregate_batters_by_season(augment_lahman_batting(stats_df))

    def validate_data(self):
        return True

    def remove_pitchers(self, stats_df, primary_pos_df):
        return (
            stats_df.merge(primary_pos_df, on=["playerID", "yearID"], how="left")
            .query(r'primaryPos != "P"')
            .drop("primaryPos", axis=1)
        )

    def seasonal_average(self, stats_df, metric_name):
        return (
            stats_df.groupby("yearID")
            .agg({metric_name: sum, "PA": sum})
            .assign(seasonal_avg=lambda row: row[metric_name] / row.PA)
        )

    def projections(self, projected_season, computed_metrics=None):
        computed_metrics = computed_metrics or self.COMPUTED_METRICS

        projections = [
            self.metric_projection(metric_name, projected_season)
            for metric_name in computed_metrics
        ]
        return pd.concat(projections, axis=1)

    def metric_projection(self, metric_name, projected_season):
        x_df = self.metric_projection_detail(metric_name, projected_season)
        return x_df.assign(
            x=lambda row: row.rate_projection
            * row.pa_projection
            * row.age_adjustment_value
        ).rename({"x": metric_name}, axis=1).loc[:, [metric_name]]

    def metric_projection_detail(self, metric_name, projected_season):
        season = projected_season - 1

        # metric_values = get_metric_values(metric_name, season)
        # seasonal_avgs = get_seasonal_avgs(metric_name, season)

        seasonal_avg_df = (
            self.seasonal_average(
                self.remove_pitchers(self.bat_df, self.primary_pos_df), metric_name
            )
            .reset_index()
            .loc[:, ["yearID", "seasonal_avg"]]
        )

        stats_df = self.bat_df.loc[:, ["playerID", "yearID", "PA", metric_name]]
        stats_df_season = stats_df.query(f"yearID == {season}").loc[
            :, ["playerID", "yearID"]
        ]

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

        pa_df = pd.concat(
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
                    .loc[:, "PA"]
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
            pa_df.values,
            self.metric_weights,
            self.pa_weights,
            sa_df.values,
        )

        pa_projection = self.compute_pa_projection(
            metric_df.values,
            pa_df.values,
            self.metric_weights,
            self.pa_weights,
            sa_df.values,
        )

        age_df = get_age(stats_df_season, self.people)
        age_values = age_df.age + 1
        age_adjustment_value = age_values.apply(age_adjustment).values

        if metric_name in self.RECIPROCAL_AGE_METRICS:
            age_adjustment_value = 1 / age_adjustment_value

        return stats_df_season.assign(
            yearID = projected_season,
            rate_projection=rate_projection,
            pa_projection=pa_projection,
            age_adjustment_value=age_adjustment_value,
        ).set_index(["playerID", "yearID"])

    def compute_rate_projection(
        self,
        metric_values,
        pa_values,
        metric_weights,
        pa_weights,
        seasonal_averages,
        num_regression_pa=100,
    ):
        pa_values[pa_values == 0] = sys.float_info.min
        normalized_metric_weights = np.array(metric_weights) / sum(metric_weights)
        unregressed_player_projection = np.sum(
            metric_values * normalized_metric_weights, 1
        )

        mean_rate_projection = np.sum(
            seasonal_averages * pa_values * normalized_metric_weights, 1
        ) / np.sum(pa_values * normalized_metric_weights, 1)

        projection_numerator = (
            unregressed_player_projection + num_regression_pa * mean_rate_projection
        )
        projection_denominator = (
            np.sum(pa_values * normalized_metric_weights, 1) + num_regression_pa
        )

        return projection_numerator / projection_denominator

    def compute_pa_projection(
        self,
        metric_values,
        pa_values,
        metric_weights,
        pa_weights,
        seasonal_averages,
        num_regression_pa=200,
    ):

        return np.sum(pa_values * pa_weights, 1) + num_regression_pa


if __name__ == "__main__":
    from pybaseballdatana.data import LahmanData

    ld = LahmanData()

    md = MarcelProjectionsBatting(ld.batting)

    import time

    start = time.time()
    cnt = 0
    for m in md.COMPUTED_METRICS:
        for season in range(1981, 2019):
            cnt += 1
            res = md.metric_projection(m, season)
            # print(res)
            # print(res[res.playerID.str.contains("^bel")])
    end = time.time()
    dt = end - start
    print(dt, dt / cnt)
