"""
===============
Statcast Data
===============


"""

from pybbda.data import StatcastData

statcast_data = StatcastData()
df = statcast_data.sc_2019_05_01
print(df)
