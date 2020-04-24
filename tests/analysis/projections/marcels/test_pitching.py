
from pybaseballdatana.analysis.projections.marcels import MarcelProjectionsPitching
from pandas import DataFrame
import pytest

def test_pitching_projections():

    md = MarcelProjectionsPitching()
    proj = md.projections(2004)
    assert int(proj.SO.max()) == 207

def test_pitching_bad_data():
    stats_df = DataFrame({"x": [1,2,3]})
    with pytest.raises(ValueError):
        MarcelProjectionsPitching(stats_df=stats_df)

