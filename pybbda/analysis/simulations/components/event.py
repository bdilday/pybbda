import attr
from enum import Enum
from pybbda.analysis.utils import check_between_zero_one
from collections import namedtuple

_DEFAULT_BATTING_EVENT_PROBS = (0, 0, 0, 0, 0)
_DEFAULT_RUNNING_EVENT_PROBS = (0.26, 0.01, 0.41, 0.60)


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


RunningEvent = namedtuple(
    "RunningEvent",
    (
        "first_base_running_event",
        "second_base_running_event",
        "third_base_running_event",
    ),
)


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
        if not 0 <= partial_sum <= 1:
            raise ValueError(
                "The sum of event probabilities "
                "must be between zero and one, not {}".format(partial_sum)
            )
        # https://www.attrs.org/en/stable/init.html#post-init-hook
        object.__setattr__(self, "out", 1 - partial_sum)

    @property
    def probs(self):
        return (
            self.out,
            self.base_on_balls,
            self.single,
            self.double,
            self.triple,
            self.home_run,
        )


@attr.s(frozen=True)
class RunningEventProbability:
    first_to_third_on_single = attr.ib(
        type=float,
        validator=check_between_zero_one,
        default=_DEFAULT_RUNNING_EVENT_PROBS[0],
    )
    first_to_home_on_single = attr.ib(
        type=float,
        validator=check_between_zero_one,
        default=_DEFAULT_RUNNING_EVENT_PROBS[1],
    )
    first_to_home_on_double = attr.ib(
        type=float,
        validator=check_between_zero_one,
        default=_DEFAULT_RUNNING_EVENT_PROBS[2],
    )
    second_to_home_on_single = attr.ib(
        type=float,
        validator=check_between_zero_one,
        default=_DEFAULT_RUNNING_EVENT_PROBS[3],
    )

    def __attrs_post_init__(self):
        first_base_partial_sum = (
            self.first_to_third_on_single + self.first_to_home_on_single
        )
        if not 0 <= first_base_partial_sum <= 1:
            raise ValueError(
                "The sum of first-base-on-single event probabilities "
                "must be between zero and one, not {}".format(first_base_partial_sum)
            )
        # https://www.attrs.org/en/stable/init.html#post-init-hook
        object.__setattr__(
            self, "first_to_second_on_single", 1 - first_base_partial_sum
        )
        object.__setattr__(
            self, "first_to_third_on_double", 1 - self.first_to_home_on_double
        )
        object.__setattr__(
            self, "second_to_third_on_single", 1 - self.second_to_home_on_single
        )

    @property
    def probs(self):
        return (
            self.first_to_third_on_single,
            self.first_to_home_on_single,
            self.first_to_home_on_double,
            self.second_to_home_on_single,
        )


@attr.s(frozen=True)
class GameEvent:
    """
    Class for a `GameEvent`. A `GameEvent` is a `BattingEvent`
    a `FirstBaseRunningEvent`, a `SecondBaseRunningEvent`, and
    a `ThirdBaseRunningEvent`
    """

    batting_event = attr.ib(type=BattingEvent)
    first_base_running_event = attr.ib(
        type=FirstBaseRunningEvent, default=FirstBaseRunningEvent.DEFAULT
    )
    second_base_running_event = attr.ib(
        type=SecondBaseRunningEvent, default=SecondBaseRunningEvent.DEFAULT
    )
    third_base_running_event = attr.ib(
        type=ThirdBaseRunningEvent, default=ThirdBaseRunningEvent.DEFAULT
    )
