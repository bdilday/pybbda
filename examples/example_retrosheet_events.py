"""
==================
Retrosheet Events
==================

"""


from pybaseballdatana.data import RetrosheetData

retrosheet_data = RetrosheetData()

print(retrosheet_data.df_from_team_id("1982OAK"))


print(
    retrosheet_data.df_from_file(
        "https://raw.githubusercontent.com/"
        "chadwickbureau/retrosheet/master/event/regular/"
        "1982OAK.EVA"
    )
)
