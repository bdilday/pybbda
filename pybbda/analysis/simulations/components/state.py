import attr
from functools import lru_cache

from pybbda.analysis.simulations.components.event import (
    BattingEvent,
    FirstBaseRunningEvent,
    SecondBaseRunningEvent,
    ThirdBaseRunningEvent,
)
from pybbda.analysis.utils import check_is_zero_one
from pybbda.analysis.simulations.constants import MAX_OUTS, INNING_OUTS


@attr.s(frozen=True)
class BaseState:
    """
    A class to represent a base state. An occupied base is
    represented by a 1 and an empty base by a 0.
    """

    first_base = attr.ib(type=int, validator=check_is_zero_one)
    second_base = attr.ib(type=int, validator=check_is_zero_one)
    third_base = attr.ib(type=int, validator=check_is_zero_one)

    def __iter__(self):
        yield self.first_base
        yield self.second_base
        yield self.third_base

    def evolve(
        self,
        batting_event,
        first_base_running_event=FirstBaseRunningEvent.DEFAULT,
        second_base_running_event=SecondBaseRunningEvent.DEFAULT,
        third_base_running_event=ThirdBaseRunningEvent.DEFAULT,
    ):

        if batting_event == BattingEvent.OUT:
            base_state = attr.evolve(self)

        elif batting_event == BattingEvent.BASE_ON_BALLS:
            base_state = BaseState(
                first_base=1,
                second_base=1 if self.first_base == 1 else self.second_base,
                third_base=1
                if self.first_base == 1 and self.second_base == 1
                else self.third_base,
            )

        elif batting_event == BattingEvent.SINGLE:

            running_events = get_running_events_cached(
                batting_event,
                first_base_running_event,
                second_base_running_event,
                third_base_running_event,
            )[0:2]

            if running_events == (
                FirstBaseRunningEvent.FIRST_TO_SECOND,
                SecondBaseRunningEvent.SECOND_TO_THIRD,
            ):
                base_state = BaseState(
                    1, 1 if self.first_base else 0, 1 if self.second_base else 0
                )

            elif running_events == (
                FirstBaseRunningEvent.FIRST_TO_SECOND,
                SecondBaseRunningEvent.SECOND_TO_HOME,
            ):
                base_state = BaseState(1, 1 if self.first_base else 0, 0)

            elif running_events == (
                FirstBaseRunningEvent.FIRST_TO_THIRD,
                SecondBaseRunningEvent.SECOND_TO_HOME,
            ):
                base_state = BaseState(1, 0, 1 if self.first_base else 0)

            elif running_events == (
                FirstBaseRunningEvent.FIRST_TO_HOME,
                SecondBaseRunningEvent.SECOND_TO_HOME,
            ):
                base_state = BaseState(1, 0, 0)

            else:
                raise ValueError(
                    "running_events combination %s is not valid", running_events
                )
        elif batting_event == BattingEvent.DOUBLE:
            running_events = get_running_events_cached(
                batting_event,
                first_base_running_event,
                second_base_running_event,
                third_base_running_event,
            )[0]

            if running_events == FirstBaseRunningEvent.FIRST_TO_THIRD:
                base_state = BaseState(0, 1, 1 if self.first_base else 0)
            elif running_events == FirstBaseRunningEvent.FIRST_TO_HOME:
                base_state = BaseState(0, 1, 0)

        elif batting_event == BattingEvent.TRIPLE:
            base_state = BaseState(0, 0, 1)
        elif batting_event == BattingEvent.HOME_RUN:
            base_state = BaseState(0, 0, 0)
        else:
            raise ValueError(
                "evolving with batting event {} "
                "and running events %{} is not valid".format(
                    batting_event,
                    (
                        first_base_running_event,
                        second_base_running_event,
                        third_base_running_event,
                    ),
                )
            )

        return attr.evolve(
            self,
            first_base=base_state.first_base,
            second_base=base_state.second_base,
            third_base=base_state.third_base,
        )


@lru_cache(maxsize=1024)
def base_state_evolve_cached(
    cls,
    batting_event,
    first_base_running_event=FirstBaseRunningEvent.DEFAULT,
    second_base_running_event=SecondBaseRunningEvent.DEFAULT,
    third_base_running_event=ThirdBaseRunningEvent.DEFAULT,
):
    """
    A function to call the `evolve` method of a `BaseState`.
    This is identical to the `BaseState.evolve` method,
    but implemented as a function to simplify application of
    an `functools.lru_cache` decorator.

    :param cls: An instance of a `BaseState`
    :param batting_event: `BattingEvent`
    :param first_base_running_event:
    :param second_base_running_event:
    :param third_base_running_event:
    :return: `BaseState`
    """
    return cls.evolve(
        batting_event,
        first_base_running_event=first_base_running_event,
        second_base_running_event=second_base_running_event,
        third_base_running_event=third_base_running_event,
    )


@lru_cache(maxsize=8192)
def base_out_state_evolve_cached(
    cls,
    batting_event,
    first_base_running_event=FirstBaseRunningEvent.DEFAULT,
    second_base_running_event=SecondBaseRunningEvent.DEFAULT,
    third_base_running_event=ThirdBaseRunningEvent.DEFAULT,
):
    """
    A function to call the `evolve` method of a `BaseOutState`.
    This is identical to the `BaseOutState.evolve` method,
    but implemented as a function to simplify application of
    an `functools.lru_cache` decorator.

    :param cls: An instance of a `BaseOutState`
    :param batting_event: `BattingEvent`
    :param first_base_running_event:
    :param second_base_running_event:
    :param third_base_running_event:
    :return: `BaseOutState`
    """
    return cls.evolve(
        batting_event,
        first_base_running_event=first_base_running_event,
        second_base_running_event=second_base_running_event,
        third_base_running_event=third_base_running_event,
    )


@lru_cache(maxsize=1024)
def runs_scored_cached(initial_state, end_state):
    """
    A function to call the `runs_scored` staticmethod of the `BaseOutState` class
    and apply an `functools.lru_cache`

    :param initial_state: `BaseOutState`
    :param end_state: `BaseOutState`
    :return: int
    """
    return BaseOutState.runs_scored(initial_state, end_state)


@lru_cache(maxsize=1024)
def get_running_events_cached(
    batting_event,
    first_base_running_event,
    second_base_running_event,
    third_base_running_event,
):
    """
    A function to apply the `get_running_events staticmethod of
    the `BaseOutState` class and apply an `functools.lru_cache`

    :param batting_event:
    :param first_base_running_event:
    :param second_base_running_event:
    :param third_base_running_event:
    :return: `RunEvents`
    """
    return BaseOutState.get_running_events(
        batting_event,
        first_base_running_event,
        second_base_running_event,
        third_base_running_event,
    )


@lru_cache(maxsize=1024)
def validate_running_events_cached(
    first_base_running_event, second_base_running_event, third_base_running_event
):
    """
    A function to validate that running events are self consistent, i.e. that
    if first base runner goes to third or home, it's not blocked by the
    second-base runner.

    :param first_base_running_event:
    :param second_base_running_event:
    :param third_base_running_event:

    :return: None
    :raises: `ValueError`
    """
    return BaseOutState._validate_running_events(
        first_base_running_event, second_base_running_event, third_base_running_event
    )


@attr.s(frozen=True)
class BaseOutState:
    base_state = attr.ib(type=BaseState)
    outs = attr.ib(type=int)
    max_outs = attr.ib(type=int, default=MAX_OUTS)

    @staticmethod
    def runs_scored(initial_state, end_state):
        """
        Computes the runs scored from state `initial_state` to state `end_state`.
        The computation is based on the assumption that the number of base runners
        plus the number of outs in the end state is equal to the number of base runners
        plus the number of outs in the start state plus one (the batter) minus the runs.

        :param initial_state: `BaseOutState`
        :param end_state: `BaseOutState`
        :return: int

        :raises: `ValueError` if runs scored is less than zero
        """
        # runs = -d(runners) - d(outs) + 1
        if end_state.outs % INNING_OUTS == 0 and end_state.outs > initial_state.outs:
            return 0
        if end_state.outs == MAX_OUTS:
            return 0
        runners_end = sum(end_state.base_state)
        runners_start = sum(initial_state.base_state)
        delta_runners = runners_end - runners_start
        delta_outs = end_state.outs - initial_state.outs
        if delta_runners + delta_outs > 1:
            raise ValueError(
                f"delta runners {delta_runners} "
                f"and delta outs {delta_outs} "
                f"implies runs scored is {1-delta_runners-delta_outs} which is invalid"
            )
        return 1 - delta_runners - delta_outs

    @staticmethod
    def get_running_events(
        batting_event,
        first_base_running_event,
        second_base_running_event,
        third_base_running_event,
    ):
        if batting_event == BattingEvent.SINGLE:
            running_events = (
                (
                    FirstBaseRunningEvent.FIRST_TO_SECOND
                    if first_base_running_event == FirstBaseRunningEvent.DEFAULT
                    else first_base_running_event
                ),
                (
                    SecondBaseRunningEvent.SECOND_TO_THIRD
                    if second_base_running_event == SecondBaseRunningEvent.DEFAULT
                    else second_base_running_event
                ),
                (
                    ThirdBaseRunningEvent.THIRD_TO_HOME
                    if third_base_running_event == ThirdBaseRunningEvent.DEFAULT
                    else third_base_running_event
                ),
            )
        elif batting_event == BattingEvent.DOUBLE:
            running_events = (
                (
                    FirstBaseRunningEvent.FIRST_TO_THIRD
                    if first_base_running_event == FirstBaseRunningEvent.DEFAULT
                    else first_base_running_event
                ),
                (
                    SecondBaseRunningEvent.SECOND_TO_HOME
                    if second_base_running_event == SecondBaseRunningEvent.DEFAULT
                    else second_base_running_event
                ),
                (
                    ThirdBaseRunningEvent.THIRD_TO_HOME
                    if third_base_running_event == ThirdBaseRunningEvent.DEFAULT
                    else third_base_running_event
                ),
            )
        else:
            running_events = (
                first_base_running_event,
                second_base_running_event,
                third_base_running_event,
            )
        BaseOutState._validate_running_events(*running_events)
        return running_events

    @staticmethod
    def _validate_running_events(
        first_base_running_event, second_base_running_event, third_base_running_event
    ):
        if (
            first_base_running_event == FirstBaseRunningEvent.FIRST_TO_THIRD
            or first_base_running_event == FirstBaseRunningEvent.FIRST_TO_HOME
        ) and second_base_running_event != SecondBaseRunningEvent.SECOND_TO_HOME:
            raise ValueError(
                "running events are not consistent %s",
                (
                    first_base_running_event,
                    second_base_running_event,
                    third_base_running_event,
                ),
            )

    def evolve(
        self,
        batting_event,
        first_base_running_event=FirstBaseRunningEvent.DEFAULT,
        second_base_running_event=SecondBaseRunningEvent.DEFAULT,
        third_base_running_event=ThirdBaseRunningEvent.DEFAULT,
    ):

        outs = self.outs

        if outs == self.max_outs:
            base_state = attr.evolve(self)
        elif batting_event == BattingEvent.OUT:
            outs = self.outs + 1
            if outs % INNING_OUTS == 0:
                base_state = BaseState(0, 0, 0)
            else:
                base_state = base_state_evolve_cached(
                    self.base_state,
                    batting_event=batting_event,
                    first_base_running_event=first_base_running_event,
                    second_base_running_event=second_base_running_event,
                    third_base_running_event=third_base_running_event,
                )
        else:
            base_state = base_state_evolve_cached(
                self.base_state,
                batting_event=batting_event,
                first_base_running_event=first_base_running_event,
                second_base_running_event=second_base_running_event,
                third_base_running_event=third_base_running_event,
            )

        return attr.evolve(self, base_state=base_state, outs=outs)


@attr.s(hash=True)
class GameState:
    base_out_state = attr.ib(
        type=BaseOutState, default=BaseOutState(BaseState(0, 0, 0), 0)
    )
    pa_count = attr.ib(type=int, default=1)
    lineup_slot = attr.ib(type=int, default=1)
    score = attr.ib(type=int, default=0)

    @staticmethod
    def pa_count_to_lineup_slot(pa_count):
        return ((pa_count - 1) % 9) + 1

    def evolve(
        self,
        batting_event,
        first_base_running_event=FirstBaseRunningEvent.DEFAULT,
        second_base_running_event=SecondBaseRunningEvent.DEFAULT,
        third_base_running_event=ThirdBaseRunningEvent.DEFAULT,
    ):
        base_out_state = base_out_state_evolve_cached(
            self.base_out_state,
            batting_event,
            first_base_running_event,
            second_base_running_event,
            third_base_running_event,
        )
        runs_scored = runs_scored_cached(self.base_out_state, base_out_state)
        game_state = attr.evolve(
            self,
            base_out_state=base_out_state,
            pa_count=self.pa_count + 1,
            lineup_slot=self.pa_count_to_lineup_slot(self.pa_count + 1),
            score=self.score + runs_scored,
        )

        return game_state
