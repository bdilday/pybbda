import argparse
import sys
from collections import defaultdict
import numpy as np

from pybbda.analysis.run_expectancy import MarkovSimulation
from pybbda.analysis.simulations import (
    BattingEventProbability,
    RunningEventProbability,
    Batter,
    Lineup,
    PlayerRegistry,
)

from pybbda.analysis.simulations.components.event import _DEFAULT_RUNNING_EVENT_PROBS
from pybbda.analysis.simulations.constants import MAX_OUTS

import logging

logger = logging.getLogger(__name__)


def _parse_args():
    parser = argparse.ArgumentParser("Run expectancy from Markov chains")

    parser.add_argument(
        "-i",
        "--lineup-slot-id",
        action="append",
        nargs=2,
        help=(
            "Set the lineup slot according to the player-id. "
            "The player-id is the Lahman playerID, underscore the Season. "
            "Example --lineup-slot-id 1 henderi01_1982."
            "Using slot 0 sets all unassigned slots to this player"
        ),
    )

    parser.add_argument(
        "-b",
        "--lineup-slot-batting-probs",
        action="append",
        nargs=6,
        help=(
            "Set the lineup slot according to the batting event probabilities. "
            "The probabilities are 5 numbers (BB, 1B, 2B, 3B, HR). "
            "Example --lineup-slot-id 1 0.177 0.160 0.037 0.006 0.015 "
            "Using slot 0 sets all unassigned slots to this player"
        ),
    )

    parser.add_argument(
        "--running-probs",
        type=float,
        nargs=4,
        required=False,
        default=_DEFAULT_RUNNING_EVENT_PROBS,
        help="Sets the running probs. These are the same for all lineup slots",
    )

    return parser.parse_args(sys.argv[1:])


def summarise_result(result):
    mean_score = result[-1].mean_score
    std_dev_score = result[-1].std_score
    print(
        "mean score per 27 outs = {:.4f}\n"
        "std. score per 27 outs = {:.4f}".format(
            mean_score / MAX_OUTS * 27, std_dev_score * np.sqrt(27 / MAX_OUTS)
        )
    )


def sim_player_id(player_id):
    player_registry = PlayerRegistry()
    player_registry.load_from_lahman()
    lineup1 = Lineup([player_registry.registry[player_id]] * 9)
    markov_simulation = MarkovSimulation(termination_threshold=1e-4)
    res1 = markov_simulation(lineup1)
    summarise_result(res1)


def lineup_from_args(args):
    slot_counter = defaultdict(int)
    slot_batters = {}

    # check if any players are passed by id
    if args.lineup_slot_id:
        player_registry = PlayerRegistry()
        player_registry.load_from_lahman()
        for lineup_slot, player_id in args.lineup_slot_id:
            lineup_slot = int(lineup_slot)
            slot_counter[lineup_slot] += 1
            slot_batters[lineup_slot] = player_registry.registry[player_id]

    # check if any players are passed by prob
    if args.lineup_slot_batting_probs:
        for lineup_slot_data in args.lineup_slot_batting_probs:
            lineup_slot, batting_probs = (
                int(lineup_slot_data[0]),
                [float(p) for p in lineup_slot_data[1:]],
            )
            slot_counter[lineup_slot] += 1
            slot_batters[lineup_slot] = Batter(
                player_id=f"p{lineup_slot}",
                batting_event_probabilities=BattingEventProbability(*batting_probs),
            )

    if not all(0 <= lineup_slot <= 9 for lineup_slot in slot_counter.keys()):
        raise ValueError(
            "slot must be between 0 and 9, not {}".format(slot_counter.keys())
        )

    if not all(0 <= lineup_count <= 1 for lineup_count in slot_counter.values()):
        raise ValueError(
            "each slot can have at most 1 entry, not {}".format(slot_counter)
        )

    if 0 in slot_batters.keys():
        lineup = Lineup(lineup=[slot_batters[0]] * 9)
    else:
        lineup = Lineup(lineup=[Batter(player_id="default")] * 9)

    for lineup_slot, batter in slot_batters.items():
        if lineup_slot != 0:
            lineup.set_lineup_slot(lineup_slot, batter)

    logger.debug("lineup {}".format(lineup))
    return lineup


def main():
    args = _parse_args()
    lineup = lineup_from_args(args)

    markov_simulation = MarkovSimulation(termination_threshold=1e-4)

    running_event_probs = RunningEventProbability(*args.running_probs)

    result = markov_simulation(
        lineup=lineup, running_event_probabilities=running_event_probs
    )
    summarise_result(result)


if __name__ == "__main__":
    main()
