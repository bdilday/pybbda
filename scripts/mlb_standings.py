
import requests
from pybbda.graphics.graphical_standings import plot_graphical_standings
import pandas as pd
from functools import reduce

url = (
    "https://statsapi.mlb.com/api/v1/standings"
    "?leagueId=103,104"
    "&season=2022"
    "&date=2022-04-13"
    "&standingsTypes=regularSeason,springTraining,firstHalf,secondHalf"
    "&hydrate=division,conference,sport,league,"
    "team(nextSchedule(team,gameType=[R,F,D,L,W,C],inclusive=false),"
    "previousSchedule(team,gameType=[R,F,D,L,W,C],inclusive=true))"
)



def process_team_record(team_record):
    return {"Team": team_record["team"]["teamName"],
            "W": team_record["wins"],
            "L": team_record["losses"],
            "RS_G": team_record["runsScored"]/team_record["gamesPlayed"],
            "RA_G": team_record["runsAllowed"] / team_record["gamesPlayed"]
            }

def process_record(record):
    lg_div = record["division"]["abbreviation"]
    return [{"lg_div": lg_div, **process_team_record(team_record)} for team_record in record["teamRecords"]]


payload = requests.get(url).json()
print(payload)
data = reduce(list.__add__, [process_record(record) for record in payload["records"]])
print(data)

standings = pd.DataFrame(data)
print(standings)
p = plot_graphical_standings(standings)
print(p)