import pytest

from pybbda.data import RetrosheetData


@pytest.fixture
def retrosheet_data():
    return RetrosheetData()


def test_retrosheet_data(retrosheet_data):
    event_files = retrosheet_data.event_files
    assert event_files

    event_file = event_files[-1]
    df = retrosheet_data.df_from_file(event_file)
    nrow, ncol = df.shape
    assert nrow > 1000
    assert ncol == 159


def test_retrosheet_data_from_url(retrosheet_data):
    _ = retrosheet_data.df_from_file(
        "https://raw.githubusercontent.com/"
        "chadwickbureau/retrosheet/master/event/regular/"
        "1982OAK.EVA"
    )


def test_retrosheet_data_from_team_id(retrosheet_data):
    _ = retrosheet_data.df_from_team_id("1982OAK")


def test_retrosheet_data_from_team_id_missing(retrosheet_data):
    with pytest.raises(FileNotFoundError):
        _ = retrosheet_data.df_from_team_id("1870OAK")
