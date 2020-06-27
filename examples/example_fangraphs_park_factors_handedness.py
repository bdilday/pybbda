"""
==================================
Fangraphs Park Factors Handedness
==================================


"""

import seaborn as sns
from pybbda.data import FangraphsData

fg_data = FangraphsData()
pl_col = "HR as R"
sns.barplot(
    data=fg_data.fg_park_factors_handedness_2018.sort_values(pl_col, ascending=False),
    y="Team",
    x=pl_col,
    color="steelblue",
)
