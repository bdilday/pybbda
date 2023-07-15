from pybbda.data import LahmanData

from pybbda.graphics.graphical_standings import plot_graphical_standings

import os

root = os.environ.get("PYBBDA_DATA_ROOT")
print(root)
data_root = "/home/bdilday/.pybbda/data/Lahman"
ld = LahmanData(data_root)

teams = ld.teams

import sys

if len(sys.argv) == 2:
    yr = sys.argv[1]
else:
    yr = 2019
standings = teams.query(f"yearID == {yr}")

p = plot_graphical_standings(standings)

print(p)
