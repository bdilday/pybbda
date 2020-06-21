"""
===============
Run Expectancy
===============


"""

import numpy as np

from pybaseballdatana.analysis.run_expectancy import MarkovSimulation
from pybaseballdatana.analysis.simulations import (
    #    BattingEventProbability,
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


player_registry = PlayerRegistry()
player_registry.load_from_lahman()

running_event_probs = RunningEventProbability(*DEFAULT_RUNNING_EVENT_PROBS)

markov_sim = MarkovSimulation()

lineup = Lineup(lineup=[Batter(player_id="default")] * 9)

markov_simulation = MarkovSimulation(termination_threshold=1e-4)


result = markov_simulation(
    lineup=lineup, running_event_probabilities=running_event_probs
)
summarise_result(result)
