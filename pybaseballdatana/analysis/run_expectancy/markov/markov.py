import attr
from collections import defaultdict

from pybaseballdatana.analysis.simulations import (
    GameState,
    BaseOutState,
    BaseState,
    GameEvent,
    BattingEventProbability,
    BattingEvent,
    FirstBaseRunningEvent,
    SecondBaseRunningEvent,
    ThirdBaseRunningEvent,
)
from pybaseballdatana.analysis.utils import check_between_zero_one
import pandas as pd


@attr.s(frozen=True)
class MarkovState:
    game_state = attr.ib(type=GameState)
    probability = attr.ib(type=float, validator=check_between_zero_one)

    def to_df(self):
        return pd.DataFrame(
            {
                "first_base": [self.game_state.base_out_state.base_state.first_base],
                "second_base": [self.game_state.base_out_state.base_state.second_base],
                "third_base": [self.game_state.base_out_state.base_state.third_base],
                "outs": [self.game_state.base_out_state.outs],
                "score": [self.game_state.score],
                "pa_count": [self.game_state.pa_count],
                "prob": [self.probability],
            }
        )


@attr.s(frozen=True)
class MarkovEvent:
    game_event = attr.ib(type=GameEvent)
    probability = attr.ib(type=float, validator=check_between_zero_one)


be = BattingEventProbability(0.08, 0.15, 0.05, 0.005, 0.3)
DEFAULT_PROBS = be.probs

DEFAULT_EVENTS = (
    (
        BattingEvent.OUT,
        FirstBaseRunningEvent.DEFAULT,
        SecondBaseRunningEvent.DEFAULT,
        ThirdBaseRunningEvent.DEFAULT,
    ),
    (
        BattingEvent.BASE_ON_BALLS,
        FirstBaseRunningEvent.DEFAULT,
        SecondBaseRunningEvent.DEFAULT,
        ThirdBaseRunningEvent.DEFAULT,
    ),
    (
        BattingEvent.SINGLE,
        FirstBaseRunningEvent.DEFAULT,
        SecondBaseRunningEvent.DEFAULT,
        ThirdBaseRunningEvent.DEFAULT,
    ),
    (
        BattingEvent.DOUBLE,
        FirstBaseRunningEvent.DEFAULT,
        SecondBaseRunningEvent.DEFAULT,
        ThirdBaseRunningEvent.DEFAULT,
    ),
    (
        BattingEvent.TRIPLE,
        FirstBaseRunningEvent.DEFAULT,
        SecondBaseRunningEvent.DEFAULT,
        ThirdBaseRunningEvent.DEFAULT,
    ),
    (
        BattingEvent.HOME_RUN,
        FirstBaseRunningEvent.DEFAULT,
        SecondBaseRunningEvent.DEFAULT,
        ThirdBaseRunningEvent.DEFAULT,
    ),
)

DEFAULT_MARKOV_EVENTS = list(
    [MarkovEvent(GameEvent(*e), p) for e, p in zip(DEFAULT_EVENTS, DEFAULT_PROBS)]
)




@attr.s
class MarkovSimulation:
    state = attr.ib(type=GameState, default=GameState())
    termination_threshold = attr.ib(type=float, default=1e-6)

    @staticmethod
    def state_transition(markov_state, markov_event):
        return MarkovState(
            markov_state.game_state.evolve(
                markov_event.game_event.batting_event,
                markov_event.game_event.first_base_running_event,
                markov_event.game_event.second_base_running_event,
                markov_event.game_event.third_base_running_event,
            ),
            markov_state.probability * markov_event.probability,
        )
