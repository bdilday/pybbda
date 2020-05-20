import argparse
import sys

from pybaseballdatana.analysis.run_expectancy import (
    MarkovEvent,
MarkovEvents,
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--batting-probs", type=float, nargs=5, required=True)
    parser.add_argument("--running-probs", type=float, nargs=4, required=True)

    return parser.parse_args(sys.argv[1:])


def main():
    args = _parse_args()
    print(args.batting_probs)
    print(args.running_probs)

    markov_simulation = MarkovSimulation(termination_threshold=1e-4)
    batting_event_probs = BattingEventProbability(*args.batting_probs)
    running_event_probs = RunEventProbability(*args.running_probs)
    result = markov_simulation(batting_event_probs, running_event_probs)
    print(result[-1].mean_score)

if __name__ == "__main__":
    main()
