import attr
from typing import List
from pybaseballdatana.analysis.simulations.components.state import GameState
from pybaseballdatana.analysis.run_expectancy.markov import MarkovState
from collections import defaultdict
from functools import reduce

@attr.s
class StateVector:
    _states = attr.ib(
        type=List[MarkovState],
        default=[MarkovState(game_state=GameState(), probability=1)],
    )

    @property
    def states(self):
        return self._states

    @staticmethod
    def combine_states(markov_states):
        def _update(acc, item):
            key, value = item
            acc[key] += value
            return acc

        return [MarkovState(*e) for e in reduce(_update, markov_states, defaultdict(float)).items()]
