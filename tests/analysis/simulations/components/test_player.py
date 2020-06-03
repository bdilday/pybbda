from pybaseballdatana.analysis.simulations import BattingEventProbability

from pybaseballdatana.analysis.simulations.components.player import Batter
import pytest


def test_batter_init():
    batting_event_probs = BattingEventProbability(0.5, 0, 0, 0, 0)
    batter = Batter(player_id="abc123", batting_event_probabilities=batting_event_probs)
    assert batter.batting_event_probabilities.out > 0


def test_batter_update():
    batter = Batter(player_id="abc123")
    assert batter.batting_event_probabilities.out > 0

    batter.set_batting_event_probs(base_on_balls=0.1, double=0.2)
    assert batter.batting_event_probabilities.out == pytest.approx(0.7)


def test_batter_fail():
    with pytest.raises(TypeError):
        _ = Batter()
