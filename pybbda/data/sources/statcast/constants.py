from pandas import Int32Dtype

nullable_int = Int32Dtype()

STATCAST_QUERY_DATA_SIZE_LIMIT = 40000

STATCAST_PBP_DAILY_URL_FORMAT = (
    "https://baseballsavant.mlb.com/statcast_search/csv?all=true"
    "&hfPT="
    "&hfAB="
    "&hfBBT="
    "&hfPR="
    "&hfZ="
    "&stadium="
    "&hfBBL="
    "&hfNewZones="
    "&hfGT=R%7C"
    "&hfC="
    "&hfSea={season}%7C"
    "&hfSit="
    "&player_type={player_type}"
    "&hfOuts="
    "&opponent="
    "&pitcher_throws="
    "&batter_stands="
    "&hfSA="
    "&game_date_gt={start_date}"
    "&game_date_lt={end_date}"
    "&hfInfield="
    "&team="
    "&position="
    "&hfOutfield="
    "&hfRO="
    "&home_road="
    "&hfFlag="
    "&hfPull="
    "&metric_1="
    "&hfInn="
    "&min_pitches=0"
    "&min_results=0"
    "&group_by=name"
    "&sort_col=pitches"
    "&player_event_sort=h_launch_speed"
    "&sort_order=desc"
    "&min_pas=0"
    "&type=details"
)

STATCAST_PBP_PLAYER_URL_FORMAT = (
    STATCAST_PBP_DAILY_URL_FORMAT + "&{player_id_var}={player_id}"
)

STATCAST_PBP_DAILY_DF_DATA_TYPES = {
    "pitch_type": str,
    "game_date": str,
    "player_name": str,
    "events": str,
    "description": str,
    "des": str,
    "game_type": str,
    "stand": str,
    "p_throws": str,
    "home_team": str,
    "away_team": str,
    "type": str,
    "bb_type": str,
    "inning_topbot": str,
    "sv_id": str,
    "pitch_name": str,
    "if_fielding_alignment": str,
    "of_fielding_alignment": str,
    "batter": nullable_int,
    "pitcher": nullable_int,
    "zone": nullable_int,
    "balls": nullable_int,
    "strikes": nullable_int,
    "game_year": nullable_int,
    "outs_when_up": nullable_int,
    "inning": nullable_int,
    "game_pk": nullable_int,
    "pitcher.1": nullable_int,
    "at_bat_number": nullable_int,
    "pitch_number": nullable_int,
    "home_score": nullable_int,
    "away_score": nullable_int,
    "bat_score": nullable_int,
    "fld_score": nullable_int,
    "post_away_score": nullable_int,
    "post_home_score": nullable_int,
    "post_bat_score": nullable_int,
    "post_fld_score": nullable_int,
}
