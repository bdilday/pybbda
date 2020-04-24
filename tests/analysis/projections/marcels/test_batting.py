
from pybaseballdatana.analysis.projections.marcels import MarcelProjectionsBatting
from pandas import DataFrame
import pytest

@pytest.mark.parametrize("season, expected",
                         [(2004, 42)])
def test_batting_projections(season, expected):

    md = MarcelProjectionsBatting()
    proj = md.projections(season)
    assert int(proj.HR.max()) == expected

def test_batting_bad_data():
    stats_df = DataFrame({"x": [1,2,3]})
    with pytest.raises(ValueError):
        MarcelProjectionsBatting(stats_df=stats_df)

