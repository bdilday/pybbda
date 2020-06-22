"""
======================================
Batted Ball Trajectory - Launch Angle
======================================

This computes a set of trajectories at fixed initial speed, varying the launch angle.

"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from pybbda.analysis.trajectories import BattedBallTrajectory

trajectory_calc = BattedBallTrajectory()


trajectories = pd.concat(
    [
        trajectory_calc.get_trajectory(
            initial_speed=100,
            launch_angle=a,
            launch_direction_angle=0,
            initial_spin=2500,
            spin_angle=-10,
        ).assign(launch_angle="la=" + str(a))
        for a in range(0, 76, 15)
    ],
    axis=0,
)


sns.lineplot(
    data=trajectories,
    x="y",
    y="z",
    hue="launch_angle",
    palette=sns.cubehelix_palette(rot=-0.4),
)
_ = plt.title("initial speed = 100")
