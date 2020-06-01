"""script to compute default lineup
uses retrosheet events to estimate the batting event probabilities
conditional on lineup slot. """
import argparse
import sys
import os

import pandas as pd
from numpy import where as np_where

from pybaseballdatana.data import RetrosheetData

DEFAULT_MIN_YEAR = 2010
DEFAULT_MAX_YEAR = 2019


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-year", default=DEFAULT_MIN_YEAR, type=int)
    parser.add_argument("--max-year", default=DEFAULT_MAX_YEAR, type=int)
    parser.add_argument("-o", "--output-path", required=True, help="Output CSV file")

    return parser.parse_args(sys.argv[1:])


def process_df(df):
    batting_events_df = (
        df.query("event_cd>=20 or event_cd==14 or event_cd==16 or event_cd<=3")
        .assign(event_cd=lambda row: np_where(row.event_cd == 2, 3, row.event_cd))
        .assign(event_cd=lambda row: np_where(row.event_cd == 16, 14, row.event_cd))
    )

    agg_df = batting_events_df.groupby("bat_lineup_id").agg({"n": "sum"})

    batting_event_prob_df = (
        batting_events_df.merge(agg_df, on="bat_lineup_id")
        .assign(z=lambda row: row.n_x / row.n_y)
        .sort_values(["bat_lineup_id", "event_cd"])
        .groupby(["bat_lineup_id", "event_cd"])
        .sum()
        .query("event_cd>3")
    )

    b = batting_event_prob_df.reset_index().pivot(
        index="bat_lineup_id", columns="event_cd", values="z"
    )
    b.columns = ["base_on_balls", "single", "double", "triple", "home_run"]
    return b


def main():
    args = _parse_args()
    file_ext = os.path.splitext(args.output_path)[-1]
    if file_ext != ".csv":
        raise ValueError(f"output path must have extension .csv, not {file_ext}")

    retrosheet_data = RetrosheetData()
    df = retrosheet_data.query(
        "select a.*, count(*) n from "
        "(select bat_lineup_id, event_cd from event where year_id>={} and year_id<={}) a "
        "group by bat_lineup_id, event_cd".format(args.min_year, args.max_year)
    )
    lineup_probs = process_df(df)
    lineup_probs.round(4).to_csv(args.output_path)
    print(lineup_probs)


if __name__ == "__main__":
    main()
