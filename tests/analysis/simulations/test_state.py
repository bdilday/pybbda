from pybaseballdatana.analysis.simulations.state import (
    BaseState,
    BaseOutState,
    GameState,
    BattingEvent,
    FirstBaseRunningEvent,
    SecondBaseRunningEvent,
    ThirdBaseRunningEvent,
)

from pybaseballdatana.analysis.simulations.player import Batter
import pytest


def test_bases():
    base_state1 = BaseState(first_base=1, second_base=1, third_base=0)
    base_state2 = BaseState(1, 1, 0)
    assert base_state1 == base_state2

    _ = BaseState(*(1, 1, 1))


def test_bases_fail():
    with pytest.raises(TypeError):
        _ = BaseState()

    with pytest.raises(TypeError):
        _ = BaseState(1, 1)

    with pytest.raises(TypeError):
        _ = BaseState(1, 1, 1, 1)


def test_base_outs():
    base_outs1 = BaseOutState(BaseState(0, 0, 1), 0)
    base_outs2 = BaseOutState(
        BaseState(first_base=0, second_base=0, third_base=1), outs=0
    )
    assert base_outs1 == base_outs2


def test_base_outs_evolve():
    base_outs1 = BaseOutState(BaseState(0, 0, 1), 0)
    base_outs2 = base_outs1.evolve(BattingEvent.OUT)
    assert base_outs2.outs == base_outs1.outs + 1

    base_outs1 = BaseOutState(BaseState(0, 0, 1), 0)
    base_outs2 = base_outs1.evolve(BattingEvent.BASE_ON_BALLS)
    assert base_outs2.base_state == BaseState(1, 0, 1)
    assert base_outs2.outs == base_outs1.outs


@pytest.mark.parametrize(
    "initial_state, end_state, expected_runs",
    [
        ((0, 0, 1, 0), (0, 0, 1, 1), 0),
        ((0, 0, 1, 0), (1, 0, 0, 0), 1),
        ((0, 0, 1, 0), (0, 0, 0, 0), 2),
        ((1, 1, 1, 0), (0, 1, 0, 0), 3),
        ((1, 1, 1, 0), (0, 0, 0, 0), 4),
    ],
)
def test_base_out_runs(initial_state, end_state, expected_runs):
    bo1 = BaseOutState(BaseState(*initial_state[0:3]), initial_state[3])
    bo2 = BaseOutState(BaseState(*end_state[0:3]), end_state[3])
    runs = BaseOutState.runs_scored(bo1, bo2)
    assert runs == expected_runs


def test_game_state():
    gs1 = GameState(BaseOutState(BaseState(0, 0, 0), 0), lineup_slot=1)
    gs2 = GameState()
    assert gs1 == gs2


from functools import partial


def test_base_out_running_events():
    validate_func = partial(
        BaseOutState._validate_running_events,
        third_base_running_event=ThirdBaseRunningEvent.THIRD_TO_HOME,
    )
    validate_func(
        FirstBaseRunningEvent.FIRST_TO_SECOND, SecondBaseRunningEvent.SECOND_TO_THIRD
    )
    validate_func(
        FirstBaseRunningEvent.FIRST_TO_SECOND, SecondBaseRunningEvent.SECOND_TO_HOME
    )
    validate_func(
        FirstBaseRunningEvent.FIRST_TO_THIRD, SecondBaseRunningEvent.SECOND_TO_HOME
    )

    with pytest.raises(ValueError):
        validate_func(
            FirstBaseRunningEvent.FIRST_TO_THIRD, SecondBaseRunningEvent.SECOND_TO_THIRD
        )

    with pytest.raises(ValueError):
        validate_func(
            FirstBaseRunningEvent.FIRST_TO_HOME, SecondBaseRunningEvent.SECOND_TO_THIRD
        )


def test_get_running_events():
    get_running_events_func = partial(
        BaseOutState.get_running_events,
        batting_event=BattingEvent.SINGLE,
        third_base_running_event=ThirdBaseRunningEvent.DEFAULT,
    )

    assert get_running_events_func(
        first_base_running_event=FirstBaseRunningEvent.DEFAULT,
        second_base_running_event=SecondBaseRunningEvent.DEFAULT,
    ) == (
        FirstBaseRunningEvent.FIRST_TO_SECOND,
        SecondBaseRunningEvent.SECOND_TO_THIRD,
        ThirdBaseRunningEvent.THIRD_TO_HOME,
    )
