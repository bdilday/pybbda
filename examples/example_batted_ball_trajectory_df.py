"""
======================
Batted Ball DataFrame
======================


"""


from pybaseballdatana.analysis.trajectories import BattedBallTrajectory

trajectory_calc = BattedBallTrajectory()

trajectory = trajectory_calc.get_trajectory(
    initial_speed=100,
    launch_angle=30,
    launch_direction_angle=0,
    initial_spin=2500,
    spin_angle=-10,
)
print(trajectory)
print(trajectory.z.max())
