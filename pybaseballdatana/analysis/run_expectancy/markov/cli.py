import argparse
import sys

from pybaseballdatana.analysis.run_expectancy import (
    MarkovEvent,
    MarkovState,
    MarkovSimulation,
    GameState,
    StateVector,
)
from pybaseballdatana.analysis.simulations import (
    BaseState,
    BaseOutState,
    GameState,
    Lineup,
    BattingEvent,
    RunningEvent,
    FirstBaseRunningEvent,
    SecondBaseRunningEvent,
    ThirdBaseRunningEvent,
    GameEvent,
    ALL_EVENTS,
    Batter,
    BattingEventProbability,
    Runner,
    RunEventProbability,
)


def _parse_args():
    parser = argparse.ArgumentParser(argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--batting_probs", type=float, nargs=5)
    parser.add_argument("--running_probs", type=float, nargs=4)

    return parser.parse_args(sys.argv[1:])


def main():
    args = _parse_args()
    print(args.probs)

    initial_state_vector = StateVector()


if __name__ == "__main__":
    main()
