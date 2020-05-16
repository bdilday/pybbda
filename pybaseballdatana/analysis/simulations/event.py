import attr
from enum import Enum
from pybaseballdatana.analysis.utils import check_between_zero_one

_DEFAULT_BATTING_EVENT_PROBS = (0, 0, 0, 0, 0)
_DEFAULT_RUNNING_EVENT_PROBS = (0, 0, 0, 0)


class BattingEvent(Enum):
    BASE_ON_BALLS = 0
    SINGLE = 1
    DOUBLE = 2
    TRIPLE = 3
    HOME_RUN = 4
    OUT = 5


class FirstBaseRunningEvent(Enum):
    DEFAULT = 0
    FIRST_TO_SECOND = 1
    FIRST_TO_THIRD = 2
    FIRST_TO_HOME = 3


class SecondBaseRunningEvent(Enum):
    DEFAULT = 0
    SECOND_TO_THIRD = 1
    SECOND_TO_HOME = 2


class ThirdBaseRunningEvent(Enum):
    DEFAULT = 0
    THIRD_TO_HOME = 1


@attr.s(frozen=True)
class BattingEventProbability:
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


@attr.s(frozen=True)
class RunEventProbability:
    first_to_third_on_single = attr.ib(type=float, validator=check_between_zero_one)
    first_to_home_on_single = attr.ib(type=float, validator=check_between_zero_one)
    first_to_home_on_double = attr.ib(type=float, validator=check_between_zero_one)
    second_to_home_on_double = attr.ib(type=float, validator=check_between_zero_one)
