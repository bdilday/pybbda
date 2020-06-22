"""script to estimate running event probabilities from retrosheet events"""

import argparse
import sys

from numpy import where as np_where

from pybbda.data import RetrosheetData

DEFAULT_MIN_YEAR = 2010
DEFAULT_MAX_YEAR = 2019


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-year", default=DEFAULT_MIN_YEAR, type=int)
    parser.add_argument("--max-year", default=DEFAULT_MAX_YEAR, type=int)

    return parser.parse_args(sys.argv[1:])


def process_df(df):
    grouping_columns = ["event_cd", "start_bases_cd"]
    target_column = "end_bases_cd"

    ana_df = (
        df.query("inn_ct<=8")
        .assign(event_cd=lambda row: np_where(row.event_cd == 2, 3, row.event_cd))
        .assign(event_cd=lambda row: np_where(row.event_cd == 16, 14, row.event_cd))
    )

    count_df = (
        ana_df.groupby(grouping_columns + [target_column])
        .size()
        .to_frame()
        .reset_index()
    ).rename({0: "event_ct"}, axis=1)

    return count_df.assign(
        start_first_base=lambda row: (row.start_bases_cd & 1).astype("bool"),
        start_second_base=lambda row: (row.start_bases_cd & 2).astype("bool"),
        start_third_base=lambda row: (row.start_bases_cd & 4).astype("bool"),
        end_first_base=lambda row: (row.end_bases_cd & 1).astype("bool"),
        end_second_base=lambda row: (row.end_bases_cd & 2).astype("bool"),
        end_third_base=lambda row: (row.end_bases_cd & 4).astype("bool"),
    )


def get_first_to_home_on_double(ana_df):

    first_to_third = ana_df.query(
        "event_cd==21 and start_first_base and end_third_base"
    ).event_ct.sum()
    first_to_home = ana_df.query(
        "event_cd==21 and start_first_base and ~end_third_base"
    ).event_ct.sum()
    print(first_to_third, first_to_home)
    return first_to_home / (first_to_home + first_to_third)


def get_second_to_home_on_single(ana_df):
    second_to_third = 0
    second_to_third += ana_df.query(
        "event_cd==20 and "
        "start_first_base and start_second_base "
        "and end_first_base and end_second_base and end_third_base"
    ).event_ct.sum()
    second_to_third += ana_df.query(
        "event_cd==20 and "
        "~start_first_base and start_second_base "
        "and end_first_base and end_third_base"
    ).event_ct.sum()

    second_to_home = 0
    second_to_home += ana_df.query(
        "event_cd==20 and "
        "start_first_base and start_second_base "
        "and ((end_second_base and ~end_third_base) or (~end_second_base and end_third_base))"
    ).event_ct.sum()
    second_to_home += ana_df.query(
        "event_cd==20 and "
        "~start_first_base and start_second_base "
        "and ~end_second_base and ~end_third_base"
    ).event_ct.sum()

    return second_to_home / (second_to_home + second_to_third)


def get_first_on_single(ana_df):
    first_to_home = ana_df.query(
        "event_cd==20 and start_first_base and ~start_second_base and ~end_second_base and ~end_third_base"
    ).event_ct.sum()
    first_to_third = ana_df.query(
        "event_cd==20 and start_first_base and ~start_second_base and ~end_second_base and end_third_base"
    ).event_ct.sum()
    first_to_second = ana_df.query(
        "event_cd==20 and start_first_base and ~start_second_base and end_second_base and ~end_third_base"
    ).event_ct.sum()
    total = first_to_home + first_to_third + first_to_second
    return first_to_second / total, first_to_third / total, first_to_home / total


def main():
    args = _parse_args()

    retrosheet_data = RetrosheetData()

    df = retrosheet_data.query(
        "select game_id, start_bases_cd, end_bases_cd, event_cd, outs_ct, inn_ct "
        "from event where "
        "year_id>={} and year_id<={} and "
        "(event_cd<=3 or event_cd>=20 or event_cd=14 or event_cd=16)".format(
            args.min_year, args.max_year
        )
    )

    count_df = process_df(df)
    first_to_home_on_double = get_first_to_home_on_double(count_df)
    print("first_to_home_on)double ", first_to_home_on_double)

    second_to_home_on_single = get_second_to_home_on_single(count_df)
    print("second_to_home_on_single ", second_to_home_on_single)

    print(get_first_on_single(count_df))


if __name__ == "__main__":
    main()
