from pybaseballdatana.analysis.simulations import (
    GameState,
    BattingEvent,
    BattingEventProbability,
    BaseOutState,
    BaseState,
    ALL_EVENTS,
    RunningEvent,
    RunEventProbability,
    GameEvent,
)
from pybaseballdatana.analysis.run_expectancy.markov import (
    MarkovSimulation,
    MarkovState,
    MarkovEvent,
    MarkovEvents,
)
from pybaseballdatana.analysis.run_expectancy.markov.markov import StateVector


def test_markov_simulation_transitions():
    markov_simulation = MarkovSimulation()

    initial_state = MarkovState(
        game_state=GameState(
            BaseOutState(BaseState(0, 0, 0), outs=0), lineup_slot=1, pa_count=1
        ),
        probability=1,
    )
    event = MarkovEvent(game_event=GameEvent(BattingEvent.OUT), probability=1)
    expected_state = MarkovState(
        game_state=GameState(
            base_out_state=BaseOutState(base_state=BaseState(0, 0, 0), outs=1),
            lineup_slot=2,
            pa_count=2,
        ),
        probability=1,
    )
    assert markov_simulation.state_transition(initial_state, event) == expected_state

    initial_state = MarkovState(
        game_state=GameState(
            BaseOutState(BaseState(0, 0, 0), outs=0), lineup_slot=1, pa_count=1
        ),
        probability=1,
    )
    event = MarkovEvent(game_event=GameEvent(BattingEvent.HOME_RUN), probability=1)
    expected_state = MarkovState(
        game_state=GameState(
            base_out_state=BaseOutState(base_state=BaseState(0, 0, 0), outs=0),
            lineup_slot=2,
            pa_count=2,
            score=1,
        ),
        probability=1,
    )
    assert markov_simulation.state_transition(initial_state, event) == expected_state

    initial_state = MarkovState(
        game_state=GameState(
            BaseOutState(BaseState(0, 0, 0), outs=0), lineup_slot=1, pa_count=1
        ),
        probability=0.5,
    )
    event = MarkovEvent(game_event=GameEvent(BattingEvent.HOME_RUN), probability=1)
    expected_state = MarkovState(
        game_state=GameState(
            base_out_state=BaseOutState(base_state=BaseState(0, 0, 0), outs=0),
            lineup_slot=2,
            pa_count=2,
            score=1,
        ),
        probability=0.5,
    )
    assert markov_simulation.state_transition(initial_state, event) == expected_state


def test_markov_events():
    _ = MarkovEvents([MarkovEvent(GameEvent(BattingEvent.SINGLE), 1)])

    be = BattingEventProbability(0.08, 0.15, 0.05, 0.005, 0.03)
    re = RunEventProbability(0, 0, 0, 0)
    markov_events = MarkovEvents.from_probs(be, re)
    assert markov_events.total_probability == 1

    be = BattingEventProbability(0.08, 0.15, 0.05, 0.005, 0.03)
    re = RunEventProbability(0.1, 0.1, 0.1, 0.1)
    markov_events = MarkovEvents.from_probs(be, re)
    assert markov_events.total_probability == 1


def test_markov_simulations_results():
    markov_simulation = MarkovSimulation()
    batting_event_probs = BattingEventProbability(0.5, 0, 0, 0, 0)
    running_event_probs = RunEventProbability(0, 0, 0, 0)
    markov_events = MarkovEvents.from_probs(batting_event_probs, running_event_probs)
    initial_state_vector = StateVector()
    result = markov_simulation(batting_event_probs, running_event_probs)
    assert result == 1
