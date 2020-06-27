from pybbda.data.sources.statcast.utils import get_statcast_tables


def test_get_tables():
    min_year = 2016
    max_year = 2019
    _ = get_statcast_tables(min_year, max_year)
