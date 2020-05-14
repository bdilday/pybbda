from pybaseballdatana.analysis.simulations.state import BaseState, BaseOutState
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
    base_outs2 = BaseOutState(BaseState(0, 0, 1), 0)


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
