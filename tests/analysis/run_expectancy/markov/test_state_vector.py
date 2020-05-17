from pybaseballdatana.analysis.run_expectancy.markov.state_vector import StateVector


def test_state_vector():
    sv = StateVector()
    assert len(sv.states) == 1
