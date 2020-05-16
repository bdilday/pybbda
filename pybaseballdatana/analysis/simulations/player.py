import attr
from .event import EventProbability, _DEFAULT_BATTING_EVENT_PROBS


@attr.s(kw_only=True)
class Player:
    player_id = attr.ib(type=str)


@attr.s(kw_only=True)
class Batter(Player):
    event_probabilities = attr.ib(
        default=EventProbability(*_DEFAULT_BATTING_EVENT_PROBS), type=EventProbability
    )

    def set_event_probs(self, **event_probs):
        self.event_probabilities = attr.evolve(self.event_probabilities, **event_probs)
