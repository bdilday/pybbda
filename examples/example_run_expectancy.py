"""
===============
Run Expectancy
===============


"""

import numpy as np

from pybaseballdatana.analysis.run_expectancy import MarkovSimulation
from pybaseballdatana.analysis.simulations import (
    BattingEventProbability,
    RunningEventProbability,
    Batter,
    Lineup,
    PlayerRegistry,
)

from pybaseballdatana.analysis.simulations.components.event import (
    _DEFAULT_RUNNING_EVENT_PROBS as DEFAULT_RUNNING_EVENT_PROBS,
)
from pybaseballdatana.analysis.simulations.constants import MAX_OUTS


def summarise_result(result):
    mean_score = result[-1].mean_score
    std_dev_score = result[-1].std_score
    print(
        "mean score per 27 outs = {:.4f}\n"
        "std. score per 27 outs = {:.4f}".format(
            mean_score / MAX_OUTS * 27, std_dev_score * np.sqrt(27 / MAX_OUTS)
        )
    )


def initialize_lineup():
    default_batting_probs = {
        "base_on_balls": 0.08,
        "single": 0.15,
        "double": 0.05,
        "triple": 0.005,
        "home_run": 0.03,
    }

    default_batter = Batter(
        player_id="default",
        batting_event_probabilities=BattingEventProbability(**default_batting_probs),
    )
    lineup = Lineup(lineup=[default_batter] * 9)
    return lineup


def update_lineup(lineup, lineup_slot, batter):
    lineup.set_lineup_slot(lineup_slot, batter)
    return lineup


player_registry = PlayerRegistry()
player_registry.load_from_lahman()


running_event_probs = RunningEventProbability(*DEFAULT_RUNNING_EVENT_PROBS)
print("## default running probs:\n", running_event_probs, "\n")


markov_simulation = MarkovSimulation(termination_threshold=1e-4)


lineup = initialize_lineup()
result = markov_simulation(
    lineup=lineup, running_event_probabilities=running_event_probs
)
print("## markov simulation result")
summarise_result(result)


lahman_id = "henderi01_1982"
lineup = update_lineup(lineup, 1, player_registry.registry[lahman_id])
result = markov_simulation(
    lineup=lineup, running_event_probabilities=running_event_probs
)
print("## markov simulation result")
summarise_result(result)
