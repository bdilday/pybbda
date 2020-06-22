def aggregate_by_season(stats_df):
    return stats_df.groupby(["playerID", "yearID"]).sum().reset_index()
