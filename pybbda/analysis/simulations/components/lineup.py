import attr
from functools import partial
from typing import List

from pybbda.analysis.simulations import Batter
from pybbda.analysis.utils import check_len


@attr.s
class Lineup:
    """
    Class for a lineup, which comprises 9 Batters
    """

    lineup = attr.ib(type=List[Batter], validator=partial(check_len, len_constraint=9))

    def set_lineup_slot(self, lineup_slot, batter):
        """
        Sets `lineup_slot` to `batter`. `lineup_slot` can be from 1 to 9,
        i.e. it is not 0-indexed

        :param lineup_slot: int
        :param batter: `Batter`
        :return: None
        """
        self.lineup[lineup_slot - 1] = batter

    def get_batting_probs(self, lineup_slot):
        """
        Gets the batting event probabilities for the batter in the
        lineup_slot

        :param lineup_slot: int
        :return: `BattingEventProbability`
        """
        batter = self.lineup[lineup_slot - 1]
        return batter.batting_event_probabilities
