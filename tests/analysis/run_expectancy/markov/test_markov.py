from pybaseballdatana.analysis.simulations import (
    GameState,
    BattingEvent,
    BaseOutState,
    BaseState,
    ALL_EVENTS,
    RunningEvent,
    GameEvent,
)
from pybaseballdatana.analysis.run_expectancy.markov import (
    MarkovSimulation,
    MarkovState,
    MarkovEvent,
)


def test_markov_simulation():
    _ = MarkovSimulation()


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
