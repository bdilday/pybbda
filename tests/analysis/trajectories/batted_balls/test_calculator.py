
import numpy as np
from pybaseballdatana.analysis.trajectories.batted_balls.calculator import BattedBallTrajectory

def test_batted_ball_init():
    BattedBallTrajectory()

def test_batted_ball_trajectory():
    batted_ball_traj = BattedBallTrajectory()
    launch_angle = 20
    launch_dir = 0
    initial_speed = 100
    initial_spin = None
    traj = batted_ball_traj.get_trajectory(initial_speed, initial_spin, launch_angle, launch_dir)
    assert traj.shape ==(9,9)