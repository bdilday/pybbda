import attr
from functools import partial
from typing import List

from pybaseballdatana.analysis.simulations.components.event import (
    BattingEventProbability,
    RunEventProbability,
    _DEFAULT_BATTING_EVENT_PROBS,
    _DEFAULT_RUNNING_EVENT_PROBS,
)
from pybaseballdatana.analysis.utils import check_len


@attr.s(kw_only=True)
class Player:
    player_id = attr.ib(type=str)


@attr.s(kw_only=True)
class Batter(Player):
    event_probabilities = attr.ib(
        default=BattingEventProbability(*_DEFAULT_BATTING_EVENT_PROBS),
        type=BattingEventProbability,
    )

    def set_event_probs(self, **event_probs):
        self.event_probabilities = attr.evolve(self.event_probabilities, **event_probs)


@attr.s(kw_only=True)
class Runner(Player):
    run_event_probabilities = attr.ib(
        default=RunEventProbability(*_DEFAULT_RUNNING_EVENT_PROBS),
        type=RunEventProbability,
    )

    def set_event_probs(self, **run_event_probs):
        self.run_event_probabilities = attr.evolve(
            self.run_event_probabilities, **run_event_probs
        )


@attr.s
class Lineup:
    lineup = attr.ib(type=List[Batter], validator=partial(check_len, len_constraint=9))

    def set_lineup_slot(self, lineup_slot, batter):
        self.lineup[lineup_slot] = batter

    def get_batting_probs(self, lineup_slot):
        batter = self.lineup[lineup_slot - 1]
        return batter.event_probabilities
