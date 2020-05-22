from pybaseballdatana.analysis.simulations.components.event import (
    BattingEvent,
    FirstBaseRunningEvent,
    SecondBaseRunningEvent,
    ThirdBaseRunningEvent,
    BattingEventProbability,
    RunEventProbability,
)
import pytest


def test_running_event():
    assert len(list(FirstBaseRunningEvent)) == 4
    assert len(list(SecondBaseRunningEvent)) == 3
    assert len(list(ThirdBaseRunningEvent)) == 2


def test_batting_event():
    assert len(list(BattingEvent)) == 6


def test_event_probability():
    event_probs = BattingEventProbability(
        base_on_balls=0.1, single=0.1, double=0.1, triple=0.1, home_run=0.1
    )
    assert event_probs.out == pytest.approx(0.5)


def test_run_event_probability():
    re = RunEventProbability(
        first_to_third_on_single=0.1,
        first_to_home_on_single=0.2,
        first_to_home_on_double=0.3,
        second_to_home_on_single=0.4,
    )
    assert re.first_to_second_on_single == pytest.approx(0.7)
    assert re.first_to_third_on_double == pytest.approx(0.7)
    assert re.second_to_third_on_single == pytest.approx(0.6)

    _ = RunEventProbability(0, 0, 0, 0)

    with pytest.raises(ValueError):
        _ = RunEventProbability(1.1, 0, 0, 0)

    with pytest.raises(ValueError):
        _ = RunEventProbability(-1.1, 0, 0, 0)

    with pytest.raises(ValueError):
        _ = RunEventProbability(0.5, 0.51, 0, 0)


def test_event_probability_fails():
    with pytest.raises(ValueError):
        BattingEventProbability(
            base_on_balls=0.1, single=0.1, double=0.1, triple=0.1, home_run=0.61
        )
