"""
=======
Lahman
=======

This shows how to access the Lahman data

"""

from matplotlib import pyplot as plt
from pybaseballdatana.data import LahmanData

lahman_data = LahmanData()

batter_df = lahman_data.batting

print(batter_df)

