import attr
from collections import defaultdict
from typing import List
from pybaseballdatana.analysis.simulations.components.state import (
    base_out_state_evolve_fun,
)
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


@attr.s(frozen=True)
class MarkovEvents:
    events = attr.ib(type=List[MarkovEvent])

    @property
    def total_probability(self):
        return sum([event.probability for event in self.events])

    @staticmethod
    def from_players(
        batter, first_base_runner=None, second_base_runner=None, third_base_runner=None
    ):
        pass

    @staticmethod
    def from_probs(batting_event_probs, running_event_probs):
        total_prob_on_singles = (
            running_event_probs.first_to_second_on_single
            + (
                running_event_probs.first_to_third_on_single
                + running_event_probs.first_to_home_on_single
            )
            * running_event_probs.second_to_home_on_single
        )
        total_prob_on_singles_inv = 1 / total_prob_on_singles
        events = [
            (
                GameEvent(
                    BattingEvent.OUT,
                    FirstBaseRunningEvent.DEFAULT,
                    SecondBaseRunningEvent.DEFAULT,
                    ThirdBaseRunningEvent.DEFAULT,
                ),
                batting_event_probs.out,
            ),
            (
                GameEvent(
                    BattingEvent.BASE_ON_BALLS,
                    FirstBaseRunningEvent.DEFAULT,
                    SecondBaseRunningEvent.DEFAULT,
                    ThirdBaseRunningEvent.DEFAULT,
                ),
                batting_event_probs.base_on_balls,
            ),
            (
                GameEvent(
                    BattingEvent.SINGLE,
                    FirstBaseRunningEvent.DEFAULT,
                    SecondBaseRunningEvent.DEFAULT,
                    ThirdBaseRunningEvent.DEFAULT,
                ),
                batting_event_probs.single
                * (
                    1
                    - running_event_probs.first_to_third_on_single
                    - running_event_probs.first_to_home_on_single
                )
                * (1 - running_event_probs.second_to_home_on_single)
                * total_prob_on_singles_inv,
            ),
            (
                GameEvent(
                    BattingEvent.SINGLE,
                    FirstBaseRunningEvent.DEFAULT,
                    SecondBaseRunningEvent.SECOND_TO_HOME,
                    ThirdBaseRunningEvent.DEFAULT,
                ),
                batting_event_probs.single
                * (
                    1
                    - running_event_probs.first_to_third_on_single
                    - running_event_probs.first_to_home_on_single
                )
                * running_event_probs.second_to_home_on_single
                * total_prob_on_singles_inv,
            ),
            (
                GameEvent(
                    BattingEvent.SINGLE,
                    FirstBaseRunningEvent.FIRST_TO_THIRD,
                    SecondBaseRunningEvent.SECOND_TO_HOME,
                    ThirdBaseRunningEvent.DEFAULT,
                ),
                batting_event_probs.single
                * running_event_probs.first_to_third_on_single
                * running_event_probs.second_to_home_on_single
                * total_prob_on_singles_inv,
            ),
            (
                GameEvent(
                    BattingEvent.SINGLE,
                    FirstBaseRunningEvent.FIRST_TO_HOME,
                    SecondBaseRunningEvent.SECOND_TO_HOME,
                    ThirdBaseRunningEvent.DEFAULT,
                ),
                batting_event_probs.single
                * running_event_probs.first_to_home_on_single
                * running_event_probs.second_to_home_on_single
                * total_prob_on_singles_inv,
            ),
            (
                GameEvent(
                    BattingEvent.DOUBLE,
                    FirstBaseRunningEvent.DEFAULT,
                    SecondBaseRunningEvent.DEFAULT,
                    ThirdBaseRunningEvent.DEFAULT,
                ),
                batting_event_probs.double
                * (1 - running_event_probs.first_to_home_on_double),
            ),
            (
                GameEvent(
                    BattingEvent.DOUBLE,
                    FirstBaseRunningEvent.FIRST_TO_HOME,
                    SecondBaseRunningEvent.DEFAULT,
                    ThirdBaseRunningEvent.DEFAULT,
                ),
                batting_event_probs.double
                * running_event_probs.first_to_home_on_double,
            ),
            (
                GameEvent(
                    BattingEvent.TRIPLE,
                    FirstBaseRunningEvent.DEFAULT,
                    SecondBaseRunningEvent.DEFAULT,
                    ThirdBaseRunningEvent.DEFAULT,
                ),
                batting_event_probs.triple,
            ),
            (
                GameEvent(
                    BattingEvent.HOME_RUN,
                    FirstBaseRunningEvent.DEFAULT,
                    SecondBaseRunningEvent.DEFAULT,
                    ThirdBaseRunningEvent.DEFAULT,
                ),
                batting_event_probs.home_run,
            ),
        ]

        return MarkovEvents([MarkovEvent(*e) for e in events])


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
            base_out_state_evolve_fun(
                markov_state.game_state,
                markov_event.game_event.batting_event,
                markov_event.game_event.first_base_running_event,
                markov_event.game_event.second_base_running_event,
                markov_event.game_event.third_base_running_event,
            ),
            markov_state.probability * markov_event.probability,
        )
