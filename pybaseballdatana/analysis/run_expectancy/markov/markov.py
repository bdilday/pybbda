import attr
from pybaseballdatana.analysis.simulations import (
    GameState,
    BaseOutState,
    BaseState,
    GameEvent,
)
from collections import namedtuple

MarkovState = namedtuple("MarkovState", ("game_state", "probability"))
MarkovEvent = namedtuple("MarkovEvent", ("game_event", "probability"))


@attr.s
class MarkovSimulation:
    state = attr.ib(type=GameState, default=GameState())
    termination_threshold = attr.ib(type=float, default=1e-6)

    def state_transition(self, markov_state, markov_event):
        return MarkovState(
            markov_state.game_state.evolve(
                markov_event.game_event.batting_event,
                markov_event.game_event.first_base_running_event,
                markov_event.game_event.second_base_running_event,
                markov_event.game_event.third_base_running_event,
            ),
            markov_state.probability * markov_event.probability,
        )
