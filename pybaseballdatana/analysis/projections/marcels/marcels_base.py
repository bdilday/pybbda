from abc import ABC
from pybaseballdatana.data import LahmanData

import pandas as pd
import numpy as np
from pybaseballdatana.data.tools.processing.aggregate import aggregate_by_season
from pybaseballdatana.data.tools.processing.transform import get_age
from pybaseballdatana.data.tools.lahman.data import (
    get_primary_position,
    augment_lahman_batting,
)
from pybaseballdatana.data import LahmanData
import sys
from pybaseballdatana.analysis.projections.marcels.age_adjustment import age_adjustment


class MarcelsProjectionsBase(ABC):
    COMPUTED_METRICS = []
    RECIPROCAL_AGE_METRICS = []
    LEAGUE_AVG_PT = None
    NUM_REGRESSION_PLAYING_TIME = None
    METRIC_WEIGHTS = (5, 4, 3)
    PT_WEIGHTS = (0.5, 0.1, 0)

    def __init__(self, stats_df=None, primary_pos_df=None):
        self.ld = LahmanData()

        self.stats_df = stats_df if stats_df is not None else self._load_data()
        self.validate_data(self.stats_df)
        self.stats_df = self.preprocess_data(self.stats_df)

        self.primary_pos_df = (
            get_primary_position(self.ld.fielding)
            if primary_pos_df is None
            else primary_pos_df
        )
        self.metric_weights = np.array(self.METRIC_WEIGHTS)
        self.pt_weights = np.array(self.PT_WEIGHTS)
        self.league_avg_pa = self.LEAGUE_AVG_PT
        self.people = self.ld.people

    def _load_data(self):
        NotImplemented

    def preprocess_data(self, stats_df):
        NotImplemented


    def validate_data(self, stats_df):
        missing_columns = []
        for required_column in self.REQUIRED_COLUMNS:
            if required_column not in stats_df.columns:
                missing_columns.append(required_column)
        if missing_columns:
            raise ValueError(
                "the following required columns are missing {}".format(missing_columns)
            )

    def metric_projection(self, metric_name, projected_season):
        x_df = self.metric_projection_detail(metric_name, projected_season)
        return (
            x_df.assign(
                x=lambda row: row.rate_projection
                * row.pt_projection
                * row.age_adjustment_value
                * row.rebaseline_value
            )
            .rename({"x": metric_name}, axis=1)
            .loc[:, [metric_name]]
        )

    def projections(self, projected_season, computed_metrics=None):
        computed_metrics = computed_metrics or self.COMPUTED_METRICS

        projections = [
            self.metric_projection(metric_name, projected_season)
            for metric_name in computed_metrics
        ]
        return pd.concat(projections, axis=1)

    def seasonal_average(self, stats_df, metric_name, playing_time_column):
        return (
            stats_df.groupby("yearID")
            .agg({metric_name: sum, playing_time_column: sum})
            .assign(
                seasonal_avg=lambda row: row[metric_name] / row[playing_time_column]
            )
        )

    def get_num_regression_pt(self, stats_df):
        return self.NUM_REGRESSION_PLAYING_TIME

