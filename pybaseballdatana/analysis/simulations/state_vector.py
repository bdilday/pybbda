import attr
from typing import List
from pybaseballdatana.analysis.simulations.state import GameState


@attr.s
class StateVector:
    _states = attr.ib(type=List[GameState], default=[GameState()])

    @property
    def states(self):
        return self._states
