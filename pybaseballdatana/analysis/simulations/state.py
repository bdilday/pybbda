import attr
from typing import List
from pybaseballdatana.analysis.simulations.player import Batter
from pybaseballdatana.analysis.utils import check_len
from functools import partial


@attr.s
class Bases:
    bases = attr.ib(type=List[int])


@attr.s
class BaseOutState:
    bases = attr.ib(type=Bases)
    outs = attr.ib(type=int)

    @staticmethod
    def runs_scored(initial_state, end_state):
        # runs = -d(runners) - d(outs) + 1
        runners_end = end_state.bases.bases.values.sum
        runners_start = initial_state.bases.bases.values.sum
        delta_runners = runners_end - runners_start
        delta_outs = end_state.outs - initial_state.outs
        return 1 - delta_runners - delta_outs


@attr.s
class Lineup:
    lineup = attr.ib(List[Batter], validator=partial(check_len, len_constraint=9))
