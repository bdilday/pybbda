from pybaseballdatana.data.sources.fangraphs.data import FangraphsData


def test_fangraphs_init():
    FangraphsData()


def test_fangraphs_singleton():
    fg1 = FangraphsData()
    fg2 = FangraphsData()
    assert fg1 is fg2


def test_fangraphs_guts_years():
    fg = FangraphsData()
    assert fg.fg_guts_constants.Season.min() == 1871
    assert 2019 in list(fg.fg_guts_constants.Season)


def test_fangraphs_batting():
    fg = FangraphsData()
    df = fg.fg_batting_2019


def test_fangraphs_pitching():
    fg = FangraphsData()
    df = fg.fg_pitching_2019
