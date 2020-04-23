
from pybaseballdatana.analysis.projections.marcels.marcels_batting import MarcelProjectionsBatting
from pandas import DataFrame
import pytest

def test_batting_projections():

    md = MarcelProjectionsBatting()
    proj = md.projections(2004)
    assert int(proj.HR.max()) == 41

def test_batting_bad_data():
    stats_df = DataFrame({"x": [1,2,3]})
    with pytest.raises(ValueError):
        MarcelProjectionsBatting(stats_df=stats_df)

