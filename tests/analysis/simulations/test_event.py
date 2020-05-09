from pybaseballdatana.analysis.simulations.event import BattingEvent, EventProbability
import pytest


def test_batting_event():
    assert len(list(BattingEvent)) == 6


def test_event_probability():
    event_probs = EventProbability(
        base_on_balls=0.1, single=0.1, double=0.1, triple=0.1, home_run=0.1
    )
    assert event_probs.out == pytest.approx(0.5)


def test_event_probability_fails():
    with pytest.raises(ValueError):
        EventProbability(
            base_on_balls=0.1, single=0.1, double=0.1, triple=0.1, home_run=0.61
        )
