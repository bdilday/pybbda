import argparse
import sys
import numpy as np

from pybaseballdatana.analysis.run_expectancy import MarkovSimulation
from pybaseballdatana.analysis.simulations import (
    BattingEventProbability,
    RunningEventProbability,
    Batter,
    Lineup,
    PlayerRegistry,
)

import logging

logger = logging.getLogger(__name__)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batting-probs", type=float, nargs=5, required=True)
    parser.add_argument("--running-probs", type=float, nargs=4, required=True)
    parser.add_argument("--lahman", action="store_true")
    return parser.parse_args(sys.argv[1:])


def summarise_result(result):
    print("mean_score per inning= {:.4f}".format(result[-1].mean_score))


def test_lineups():
    np.random.seed(101)
    player_registry = PlayerRegistry()
    player_registry.load_from_lahman()
    ks = list(player_registry.registry.keys())
    p1 = np.random.choice(ks, 9)
    p2 = np.random.choice(ks, 9)
    lineup1 = Lineup([player_registry.registry[k] for k in p1])
    lineup2 = Lineup([player_registry.registry[k] for k in p2])
    markov_simulation = MarkovSimulation(termination_threshold=1e-6)
    res1 = markov_simulation(lineup1)
    res2 = markov_simulation(lineup2)
    summarise_result(res1)
    summarise_result(res2)


def main():
    args = _parse_args()
    if args.lahman:
        test_lineups()
        sys.exit(0)
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
