import pytest
from pybbda.data import StatcastData


@pytest.fixture
def statcast_data():
    return StatcastData()


def test_statcast_init():
    StatcastData()


def test_statcast_get_daily(statcast_data):
    statcast_data.get_statcast_daily(
        player_type="batter", start_date="2018-01-01", end_date="2018-01-02"
    )


def test_statcast_validate_dates(statcast_data):

    with pytest.raises(ValueError):
        statcast_data.get_statcast_daily(
            player_type="batter", start_date="2018-01-01", end_date="2017-12-31"
        )


def test_statcast_validate_player_type(statcast_data):
    with pytest.raises(ValueError):
        statcast_data.get_statcast_daily(
            player_type="", start_date="2018-01-01", end_date="2018-01-02"
        )


def test_statcast_batter_data(statcast_data):
    df = statcast_data.sc_2019_05_01
    mean_ls = (
        df.query('batter == 547989 and description != "foul"')
        .loc[:, "launch_speed"]
        .mean()
    )
    assert mean_ls == pytest.approx(102.05, 0.01)
