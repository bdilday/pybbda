import pytest
from pybaseballdatana.data import LahmanData


@pytest.fixture
def lahman_data():
    return LahmanData()


def test_lahman_datadum(lahman_data):
    assert len(lahman_data.batting) == 105861


def test_missing_path(lahman_data):
    with pytest.raises(AttributeError):
        lahman_data.battingX
