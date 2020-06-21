"""
=======================================
Batted Ball Trajectory - Initial Speed
=======================================


This computes a set of trajectories at fixed launch angle, varying the initial speed.

"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from pybaseballdatana.analysis.trajectories import BattedBallTrajectory

trajectory_calc = BattedBallTrajectory()


trajectories = pd.concat(
    [
        trajectory_calc.get_trajectory(
            initial_speed=a,
            launch_angle=35,
            launch_direction_angle=0,
            initial_spin=2500,
            spin_angle=-10,
        ).assign(launch_speed="ls=" + str(a))
        for a in range(10, 116, 25)
    ],
    axis=0,
)


plt.clf()
sns.lineplot(
    data=trajectories,
    x="y",
    y="z",
    hue="launch_speed",
    palette=sns.cubehelix_palette(rot=-0.4)[0:5],
)
_ = plt.title("launch angle = 35")
