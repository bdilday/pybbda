"""
===============================
Fangraphs Batting Leaderboards
===============================


"""

from pybbda.data import FangraphsData

fg_data = FangraphsData()

print(fg_data.fg_batting_2019)

print(len(fg_data.tables))
print(list(fg_data.tables.items())[0:10])

print(fg_data.fg_guts_constants)
