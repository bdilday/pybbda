import pandas as pd


def get_primary_position(fielding_df):
    fld_combined_stints = (
        fielding_df.groupby(["playerID", "yearID", "POS"]).sum().reset_index()
    )
    gm_rank_df = (
        fld_combined_stints.groupby(["playerID", "yearID"])
        .G.rank(method="first", ascending=False)
        .to_frame()
        .rename({"G": "gm_rank"}, axis=1)
    )
    return (
        pd.concat((fld_combined_stints, gm_rank_df), axis=1)
        .query("gm_rank == 1")
        .drop("gm_rank", axis=1)
        .filter(["playerID", "yearID", "POS"])
        .rename({"POS": "primaryPos"}, axis=1)
    )


def compute_pa(bat_df):
    PA = bat_df.loc[:, "AB"].fillna(0)
    for stat in ["BB", "HBP", "SH", "SF"]:
        PA += bat_df.loc[:, stat].fillna(0)
    return PA.astype(int)


def augment_lahman_batting(bat_df):
    PA = bat_df.loc[:, "AB"].fillna(0)
    for stat in ["BB", "HBP", "SH", "SF"]:
        PA += bat_df.loc[:, stat].fillna(0)
    X1B = (
        bat_df.loc[:, "H"]
        - bat_df.loc[:, "2B"]
        - bat_df.loc[:, "3B"]
        - bat_df.loc[:, "HR"]
    )
    TB = (
        bat_df.loc[:, "HR"] * 4
        + bat_df.loc[:, "3B"] * 3
        + bat_df.loc[:, "2B"] * 2
        + X1B
    )
    return bat_df.assign(
        PA=PA.astype(int), X1B=X1B.astype(int), TB=TB.astype(int)
    ).rename({"X1B": "1B"}, axis=1)


def augment_lahman_pitching(stats_df):
    return stats_df
