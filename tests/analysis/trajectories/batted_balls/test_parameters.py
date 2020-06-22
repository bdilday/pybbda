from attr.exceptions import FrozenInstanceError
from pybbda.analysis.trajectories.batted_balls.parameters import (
    BattedBallConstants,
    UnitConversions,
)
import pytest


def test_batted_ball_constants():
    b = BattedBallConstants()
    with pytest.raises(FrozenInstanceError):
        b.mass = 1

    with pytest.raises(ValueError):
        b = BattedBallConstants(mass=-1)


def test_unit_conversions():
    u1 = UnitConversions()
    u2 = UnitConversions()
    assert u1 is u2
