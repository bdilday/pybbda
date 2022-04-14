import pytest
from pybbda.data import LahmanData


@pytest.fixture
def lahman_data():
    return LahmanData()


def test_lahman_datadum(lahman_data):
    assert len(lahman_data.batting) > 105000


def test_missing_path(lahman_data):
    with pytest.raises(AttributeError):
        lahman_data.battingX


def test_lahman_singelton():
    ld1 = LahmanData()
    ld2 = LahmanData()
    assert ld1 is ld2
