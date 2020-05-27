from pybaseballdatana.utils import Singleton
from .player import Batter


class PlayerRegistry(Singleton):
    def __init__(self, batters=None):
        self.batters = [] if batters is None else batters
        self.registry = {}

    def _add_one(self, batter):
        self.registry[batter.player_id] = Batter

    def add(self, batters):
        if not isinstance(batters, list):
            batters = [batters]
        map(self._add_one, batters)
        return self.registry

    @property
    def len(self):
        return len(self.registry)
