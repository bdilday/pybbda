FANGRAPHS_GUTS_CONSTANTS_URL = r"http://www.fangraphs.com/guts.aspx?type=cn"

FANGRAPHS_PARK_FACTORS_FORMAT = (
    r"https://www.fangraphs.com/guts.aspx" r"?type=pf" r"&season={season}" r"&teamid=0"
)

FANGRAPHS_PARK_FACTORS_HANDEDNESS_FORMAT = (
    r"https://www.fangraphs.com/guts.aspx" r"?type=pfh" r"&season={season}" r"&teamid=0"
)

FANGRAPHS_LEADERBOARD_DEFAULT_CONFIG = {
    "stats": "bat",
    "league": "all",
    "qual": 1,  # "y",
    "ind": 0,
    "season_start": 2015,
    "season_end": 2015,
    "row_limit": 100000,
    "columns": ",".join([str(i) for i in range(2, 305)]),
}

# https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season=2016&month=0&season1=2016&ind=0
# https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=c,-1,3,4,5,6,7,8,9,10&season=2015&month=0&season1=2015&ind=0&team=&rost=&age=&filter=&players=&page=1_100000

FANGRAPHS_LEADERBOARD_URL_FORMAT = (
    r"http://www.fangraphs.com/leaders.aspx"
    r"?pos=all"
    r"&stats={stats}"
    r"&lg={league}"
    r"&qual={qual}"
    r"&type=c,{columns}"
    r"&season={season_end}"
    r"&month=0"
    r"&season1={season_start}"
    r"&ind={ind}"
    r"&team=&rost=&age=&filter=&players="
    r"&page=1_{row_limit}"
)
