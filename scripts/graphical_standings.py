from pybbda.data import LahmanData

from pybbda.graphics.graphical_standings import plot_graphical_standings

ld = LahmanData()

teams = ld.teams

import sys
if len(sys.argv) == 2:
    yr = sys.argv[1]
else:
    yr = 2019
standings = teams.query(f"yearID == {yr}")

p = plot_graphical_standings(standings)

print(p)