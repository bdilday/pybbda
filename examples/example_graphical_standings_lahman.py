"""
=============================
Graphical Standings - Lahman data
=============================

"""

from pybbda.data import LahmanData
from pybbda.graphics.graphical_standings import plot_graphical_standings

ld = LahmanData()
teams = ld.teams
season = 2019
standings = teams.query(f"yearID == {season}")

p = plot_graphical_standings(standings)

print(p)
