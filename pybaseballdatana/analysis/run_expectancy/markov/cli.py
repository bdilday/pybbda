import argparse
import sys

from pybaseballdatana.analysis.run_expectancy import MarkovSimulation
from pybaseballdatana.analysis.simulations import (
    BattingEventProbability,
    RunningEventProbability,
    Batter,
    Lineup,
)

import logging

logger = logging.getLogger(__name__)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batting-probs", type=float, nargs=5, required=True)
    parser.add_argument("--running-probs", type=float, nargs=4, required=True)

    return parser.parse_args(sys.argv[1:])


def summarise_result(result):
    print("mean_score per inning= {:.4f}".format(result[-1].mean_score))


def main():
    args = _parse_args()

    markov_simulation = MarkovSimulation(termination_threshold=1e-6)
    batting_event_probs = BattingEventProbability(*args.batting_probs)
    batter = Batter(player_id="xyz", batting_event_probabilities=batting_event_probs)
    running_event_probs = RunningEventProbability(*args.running_probs)
    result = markov_simulation(
        lineup=Lineup([batter] * 9), running_event_probabilities=running_event_probs
    )
    summarise_result(result)


if __name__ == "__main__":
    main()
