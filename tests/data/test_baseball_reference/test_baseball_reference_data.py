import pytest
from pybbda.data import BaseballReferenceData


@pytest.fixture
def baseball_ref_data():
    return BaseballReferenceData()


def test_war_bat(baseball_ref_data):
    war_bat = baseball_ref_data.war_bat
    assert war_bat.year_ID.min() == 1871
    assert war_bat.year_ID.max() >= 2021


def test_war_pitch(baseball_ref_data):
    war_pitch = baseball_ref_data.war_pitch
    assert war_pitch.year_ID.min() == 1871
    assert war_pitch.year_ID.max() >= 2021


def test_missing_path(baseball_ref_data):
    with pytest.raises(AttributeError):
        baseball_ref_data.war_blah_blah
