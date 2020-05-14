import attr
from typing import List
from pybaseballdatana.analysis.simulations.player import Batter
from pybaseballdatana.analysis.utils import check_len, check_is_zero_one
from functools import partial


@attr.s(frozen=True)
class BaseState:
    first_base = attr.ib(type=int, validator=check_is_zero_one)
    second_base = attr.ib(type=int, validator=check_is_zero_one)
    third_base = attr.ib(type=int, validator=check_is_zero_one)

    def __attrs_post_init__(self):
        object.__setattr__(
            self, "bases", (self.first_base, self.second_base, self.third_base)
        )


@attr.s
class BaseOutState:
    base_state = attr.ib(type=BaseState)
    outs = attr.ib(type=int)

    @staticmethod
    def runs_scored(initial_state, end_state):
        # runs = -d(runners) - d(outs) + 1
        runners_end = sum(end_state.base_state.bases)
        runners_start = sum(initial_state.base_state.bases)
        delta_runners = runners_end - runners_start
        delta_outs = end_state.outs - initial_state.outs
        return 1 - delta_runners - delta_outs


@attr.s
class Lineup:
    lineup = attr.ib(List[Batter], validator=partial(check_len, len_constraint=9))
