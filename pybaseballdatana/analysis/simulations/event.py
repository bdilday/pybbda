import attr
from enum import Enum
from pybaseballdatana.analysis.utils import check_between_zero_one

_DEFAULT_BATTING_EVENT_PROBS = (0, 0, 0, 0, 0)


class BattingEvent(Enum):
    BASE_ON_BALLS = 0
    SINGLE = 1
    DOUBLE = 2
    TRIPLE = 3
    HOME_RUN = 4
    OUT = 5


@attr.s(frozen=True)
class EventProbability:
    base_on_balls = attr.ib(type=float, validator=check_between_zero_one)
    single = attr.ib(type=float, validator=check_between_zero_one)
    double = attr.ib(type=float, validator=check_between_zero_one)
    triple = attr.ib(type=float, validator=check_between_zero_one)
    home_run = attr.ib(type=float, validator=check_between_zero_one)

    def __attrs_post_init__(self):
        partial_sum = (
            self.base_on_balls + self.single + self.double + self.triple + self.home_run
        )
        if not 0 <= partial_sum < 1:
            raise ValueError(
                "The sum of event probabilities must be between zero and one, not {}".format(
                    partial_sum
                )
            )
        # https://www.attrs.org/en/stable/init.html#post-init-hook
        object.__setattr__(self, "out", 1 - partial_sum)
