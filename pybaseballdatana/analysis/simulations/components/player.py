import attr
from functools import partial
from typing import List

from pybaseballdatana.analysis.simulations.components.event import (
    BattingEventProbability,
    RunningEventProbability,
    _DEFAULT_BATTING_EVENT_PROBS,
    _DEFAULT_RUNNING_EVENT_PROBS,
)
from pybaseballdatana.analysis.utils import check_len


@attr.s(kw_only=True)
class Player:
    player_id = attr.ib(type=str)


@attr.s(kw_only=True)
class Batter(Player):
    batting_event_probabilities = attr.ib(
        default=BattingEventProbability(*_DEFAULT_BATTING_EVENT_PROBS),
        type=BattingEventProbability,
    )

    running_event_probabilities = attr.ib(
        default=RunningEventProbability(*_DEFAULT_RUNNING_EVENT_PROBS),
        type=RunningEventProbability,
    )

    def set_batting_event_probs(self, **batting_event_probs):
        self.batting_event_probabilities = attr.evolve(
            self.batting_event_probabilities, **batting_event_probs
        )

    def set_running_event_probs(self, **running_event_probs):
        self.running_event_probabilities = attr.evolve(
            self.running_event_probabilities, **running_event_probs
        )


@attr.s(kw_only=True)
class Runner(Player):
    running_event_probabilities = attr.ib(
        default=RunningEventProbability(*_DEFAULT_RUNNING_EVENT_PROBS),
        type=RunningEventProbability,
    )

    def set_event_probs(self, **running_event_probs):
        self.running_event_probabilities = attr.evolve(
            self.running_event_probabilities, **running_event_probs
        )


@attr.s
class Lineup:
    lineup = attr.ib(type=List[Batter], validator=partial(check_len, len_constraint=9))

    def set_lineup_slot(self, lineup_slot, batter):
        self.lineup[lineup_slot] = batter

    def get_batting_probs(self, lineup_slot):
        batter = self.lineup[lineup_slot - 1]
        return batter.batting_event_probabilities
