from functools import reduce
import multiprocessing
import itertools

import attr
from collections import defaultdict
from typing import List
from pybaseballdatana.analysis.simulations.components.state import (
    base_out_state_evolve_fun,
)
from pybaseballdatana.analysis.simulations import (
    GameState,
    GameEvent,
    BattingEventProbability,
    BattingEvent,
    FirstBaseRunningEvent,
    SecondBaseRunningEvent,
    ThirdBaseRunningEvent,
    RunEventProbability,
)
from pybaseballdatana.analysis.utils import check_between_zero_one
import pandas as pd
import logging

logger = logging.getLogger(__name__)

NUM_PROCESSES = 5
MAX_OUTS = 3


@attr.s(frozen=True)
class MarkovState:
    """
    A MarkovState comprises a `GameState` and a probability for being in that state.

    :param game_state: The GameState
    :param probability: Probability for the GameState
    """
    game_state = attr.ib(type=GameState)
    probability = attr.ib(type=float, validator=check_between_zero_one)

    def to_df(self):
        """
        Converts the MarkovState to a Pandas DataFrame.

        :return: MarkovState as a DataFrame.

        .. code-block:: python

            markov_state = MarkovState(GameState(), 1)
            markov_state.to_df()
            first_base  second_base  third_base  outs  score  pa_count  prob
                     0            0           0     0      0         1     1


        """
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
    """
    A MarkovEvent comprises a GameEvent and a probability for that event to occur

    :param game_event: The GameEvent
    :param probability: Probability for the GameEvent
    """
    game_event = attr.ib(type=GameEvent)
    probability = attr.ib(type=float, validator=check_between_zero_one)


@attr.s(frozen=True)
class MarkovEvents:
    """
    MarkovEvents comprise a list of `MarkovEvent` type

    :param events: List of `MarkovEvent`
    """
    events = attr.ib(type=List[MarkovEvent])

    def __iter__(self):
        for event in self.events:
            yield event

    @property
    def total_probability(self):
        """The total probability for the events to occur"""
        return sum([event.probability for event in self.events])

    @staticmethod
    def from_players(
        batter, first_base_runner=None, second_base_runner=None, third_base_runner=None
    ):
        pass

    @staticmethod
    def from_probs(batting_event_probs, running_event_probs):
        """
        Constructs a `MarkovEvents` from batting and running probabilities

        :param batting_event_probs: `BattingEventProbability`
        :param running_event_probs: `RunEventProbability`
        :return: `MarkovEvents`

        .. code-block:: python
            markov_events = (
                MarkovEvents.from_probs(BattingEventProbability(0.08, 0.15, 0.05, 0.005, 0.03),
                                        RunEventProbability(0.1, 0.1, 0.1, 0.1)
                                        )
                            )

        """
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




@attr.s
class StateVector:
    """
    A StateVector comprises a List of `MarkovState` objects

    :param _states: List of `MarkovState`
    """
    _states = attr.ib(
        type=List[MarkovState],
        default=[MarkovState(game_state=GameState(), probability=1)],
    )

    def __iter__(self):
        for state in self.states:
            yield state

    def to_df(self):
        """
        Converts `StateVector` object to Pandas DataFrame

        :return:

        .. code-block:: python
            state_vector = StateVector()
            state_vector.to_df()
            first_base  second_base  third_base  outs  score  pa_count  prob
                     0            0           0     0      0         1     1

        """
        return pd.concat([MarkovState.to_df(state) for state in self.states], axis=0)

    @property
    def mean_score(self):
        """
        Mean score of the state vector

        :return: The mean score of the state
        """
        return sum([s.probability * s.game_state.score for s in self])

    @property
    def end_probability(self):
        """
        Proability for the state vector to be in an end state, example having 3 outs

        :return: Probability of being in an end state
        """
        return sum(
            [
                s.probability
                for s in self
                if s.game_state.base_out_state.outs == MAX_OUTS
            ]
        )

    @property
    def states(self):
        return self._states

    @staticmethod
    def combine_states(markov_states):
        """
        Combines a list of `MarkovState`. It deduplicates states and sums the probabilities.

        :param markov_states: List of `MarkovState`
        :return: `StateVector`

        """
        # TODO: include example in doc string
        def _update(acc, item):
            acc[item.game_state] += item.probability
            return acc

        return StateVector(
            [
                MarkovState(*e)
                for e in reduce(_update, markov_states, defaultdict(float)).items()
            ]
        )


@attr.s
class MarkovSimulation:
    state_vector = attr.ib(
        type=StateVector, default=StateVector([MarkovState(GameState(), 1)])
    )
    termination_threshold = attr.ib(type=float, default=1e-6)

    def __call__(self, batting_event_probs, running_event_probs):
        markov_events = MarkovEvents.from_probs(
            batting_event_probs, running_event_probs
        )
        ncall = 0
        MAX_CALL = 100
        state_vector = self.state_vector
        results = [state_vector]
        while (
            ncall < MAX_CALL
            and state_vector.end_probability < 1 - self.termination_threshold
        ):
            state_vector = self.markov_step(state_vector, markov_events)
            results.append(state_vector)
            ncall += 1
        if ncall >= MAX_CALL:
            approx_error = results[-1].mean_score - results[-2].mean_score
            # TODO: compute error based on second derivative
            logger.warning(
                "ncall exceed max call. approximate error is TODO", approx_error
            )

        return results

    @staticmethod
    def state_vectors_to_df(state_vectors):
        return pd.concat(
            [state_vector.to_df() for state_vector in state_vectors], axis=0
        )

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

    @staticmethod
    def state_transition_tuple(markov_state_event):
        return MarkovSimulation.state_transition(*markov_state_event)

    @staticmethod
    def markov_step(state_vector, markov_events):
        with multiprocessing.Pool(NUM_PROCESSES) as mp:
            return StateVector.combine_states(
                mp.map(
                    MarkovSimulation.state_transition_tuple,
                    itertools.product(state_vector, markov_events),
                )
            )
