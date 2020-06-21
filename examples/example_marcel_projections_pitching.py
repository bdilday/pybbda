"""
=============================
Marcel Projections - Pitching
=============================

"""

from pybaseballdatana.analysis.projections import MarcelProjectionsPitching

pitching_marcels = MarcelProjectionsPitching()
print(
    pitching_marcels.projections(projected_season=2020)
    .sort_values("SO", ascending=False)
    .head(5)
)
