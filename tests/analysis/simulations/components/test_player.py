from pybaseballdatana.analysis.simulations.components.player import Batter
import pytest


def test_batter_init():
    batter = Batter(player_id="abc123")
    assert batter.event_probabilities.out > 0


def test_batter_update():
    batter = Batter(player_id="abc123")
    assert batter.event_probabilities.out > 0

    batter.set_event_probs(base_on_balls=0.1, double=0.2)
    assert batter.event_probabilities.out == pytest.approx(0.7)


def test_batter_fail():
    with pytest.raises(TypeError):
        _ = Batter()
