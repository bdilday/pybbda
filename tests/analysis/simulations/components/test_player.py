from pybaseballdatana.analysis.simulations import BattingEventProbability

from pybaseballdatana.analysis.simulations.components.player import (
    Batter,
    Player,
    Runner,
    Lineup,
)
import pytest


def test_batter_init():
    batting_event_probs = BattingEventProbability(0.5, 0, 0, 0, 0)
    batter = Batter(player_id="abc123", event_probabilities=batting_event_probs)
    assert batter.event_probabilities.out > 0


def test_batter_update():
    batter = Batter(player_id="abc123")
    assert batter.event_probabilities.out > 0

    batter.set_event_probs(base_on_balls=0.1, double=0.2)
    assert batter.event_probabilities.out == pytest.approx(0.7)


def test_batter_fail():
    with pytest.raises(TypeError):
        _ = Batter()


def test_lineup():
    batter = Batter(player_id="abc123")
    batter.set_event_probs(
        base_on_balls=0.08, single=0.15, double=0.05, triple=0.006, home_run=0.03
    )
    lineup = Lineup(lineup=[batter] * 9)

    other_batter = Batter(player_id="xyz789")
    batter.set_event_probs(
        base_on_balls=0.18, single=0.15, double=0.05, triple=0.006, home_run=0.03
    )
    lineup.set_lineup_slot(1, other_batter)
