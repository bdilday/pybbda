import datetime


def get_statcast_tables(min_year, max_year):
    tables = {}
    for season in range(min_year, max_year + 1):
        min_date_obj = datetime.datetime.strptime(f"{season}-03-15", "%Y-%m-%d")
        max_date_obj = datetime.datetime.strptime(f"{season}-11-15", "%Y-%m-%d")
        dt_count = (max_date_obj - min_date_obj).days
        date_obj_seq = [
            min_date_obj + datetime.timedelta(dt) for dt in range(dt_count + 1)
        ]
        game_dates = [
            datetime.datetime.strftime(d, "%Y-%m-%d").replace("-", "_")
            for d in date_obj_seq
        ]
        tables.update(
            {f"sc_{game_date}": f"sc_{game_date}.csv" for game_date in game_dates}
        )
    return tables
