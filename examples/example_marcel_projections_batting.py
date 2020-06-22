"""
=============================
Marcel Projections - Batting
=============================

"""

from pybbda.analysis.projections import MarcelProjectionsBatting

batting_marcels = MarcelProjectionsBatting()
print(
    batting_marcels.projections(projected_season=2020)
    .sort_values("HR", ascending=False)
    .head(5)
)
