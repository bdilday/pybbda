import attr
from functools import partial
from typing import List

from pybaseballdatana.analysis.simulations import Batter
from pybaseballdatana.analysis.utils import check_len


@attr.s
class Lineup:
    lineup = attr.ib(type=List[Batter], validator=partial(check_len, len_constraint=9))

    def set_lineup_slot(self, lineup_slot, batter):
        self.lineup[lineup_slot - 1] = batter

    def get_batting_probs(self, lineup_slot):
        batter = self.lineup[lineup_slot - 1]
        return batter.batting_event_probabilities
