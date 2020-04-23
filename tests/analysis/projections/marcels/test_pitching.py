
from pybaseballdatana.analysis.projections.marcels.marcels_pitching import MarcelProjectionsPitching

def test_pitching_projections():

    md = MarcelProjectionsPitching()
    proj = md.projections(2004)
