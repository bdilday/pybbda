import pytest
from pybbda.data import FangraphsData


@pytest.fixture
def fg_data():
    return FangraphsData()


def test_fangraphs_init():
    FangraphsData()


def test_fangraphs_singleton():
    fg1 = FangraphsData()
    fg2 = FangraphsData()
    assert fg1 is fg2


def test_fangraphs_guts_years(fg_data):
    assert fg_data.fg_guts_constants.Season.min() == 1871
    assert 2019 in list(fg_data.fg_guts_constants.Season)


def test_fangraphs_batting(fg_data):
    _ = fg_data.fg_batting_2019


def test_fangraphs_pitching(fg_data):
    _ = fg_data.fg_pitching_2019


def test_fangraphs_park_factors(fg_data):
    _ = fg_data.fg_park_factors_2018
    _ = fg_data.fg_park_factors_handedness_2018

    with pytest.raises(AttributeError):
        _ = fg_data.fg_park_factors_1870

    with pytest.raises(AttributeError):
        _ = fg_data.fg_park_factors_2101

    with pytest.raises(AttributeError):
        _ = fg_data.fg_park_factors_handedness_2001
