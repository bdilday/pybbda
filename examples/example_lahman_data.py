"""
============
Lahman Data
============


"""

from pybaseballdatana.data import LahmanData

lahman_data = LahmanData()

batter_df = lahman_data.batting

print(batter_df)
