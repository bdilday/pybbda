"""
=======
Lahman
=======

This shows how to access the Lahman data

"""

from matplotlib import pyplot as plt
from pybaseballdatana.data import LahmanData

lahman_data = LahmanData()

print(lahman_data.table)
batter_df = lahman_data.batting

print(batter_df)



