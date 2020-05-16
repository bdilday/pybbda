from pybaseballdatana.analysis.simulations.state_vector import StateVector


def test_state_vector():
    sv = StateVector()
    assert len(sv.states) == 1
