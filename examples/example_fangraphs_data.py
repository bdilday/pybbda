"""
===============
Fangraphs Data
===============


"""
from pybaseballdatana.data import FangraphsData

fg_data = FangraphsData()

print(len(fg_data.tables))
print(list(fg_data.tables.items())[0:10])

print(fg_data.fg_guts_constants)

print(fg_data.fg_batting_2019)

print(fg_data.fg_pitching_2019)

