import argparse
import sys

from pybaseballdatana.analysis.run_expectancy import MarkovSimulation
from pybaseballdatana.analysis.simulations import (
    BattingEventProbability,
    RunningEventProbability,
    Batter,
    Lineup,
    PlayerRegistry,
)

from pybaseballdatana.analysis.simulations.components.event import (
    _DEFAULT_RUNNING_EVENT_PROBS,
)
from pybaseballdatana.analysis.simulations.constants import MAX_OUTS

import logging

logger = logging.getLogger(__name__)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lineup-slot", action="append", nargs=2)
    parser.add_argument("--batting-probs", type=float, nargs=5, required=False)
    parser.add_argument(
        "--running-probs",
        type=float,
        nargs=4,
        required=False,
        default=_DEFAULT_RUNNING_EVENT_PROBS,
    )
    parser.add_argument("--player-id")
    return parser.parse_args(sys.argv[1:])


def summarise_result(result):
    print(
        "mean_score per 27 outs = {:.4f}".format(result[-1].mean_score / MAX_OUTS * 27)
    )


def sim_player_id(player_id):
    player_registry = PlayerRegistry()
    player_registry.load_from_lahman()
    lineup1 = Lineup([player_registry.registry[player_id]] * 9)
    markov_simulation = MarkovSimulation(termination_threshold=1e-4)
    res1 = markov_simulation(lineup1)
    summarise_result(res1)


def main():
    args = _parse_args()
    print(args.lineup_slot)
    #    sys.exit(1)
    if args.player_id:
        sim_player_id(player_id=args.player_id)
        sys.exit(1)
    markov_simulation = MarkovSimulation(termination_threshold=1e-4)
    batting_event_probs = BattingEventProbability(*args.batting_probs)
    batter = Batter(player_id="xyz", batting_event_probabilities=batting_event_probs)
    running_event_probs = RunningEventProbability(*args.running_probs)
    result = markov_simulation(
        lineup=Lineup([batter] * 9), running_event_probabilities=running_event_probs
    )
    summarise_result(result)


if __name__ == "__main__":
    main()
