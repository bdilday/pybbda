import attr
from scipy.integrate import RK45
import numpy as np
import pandas as pd
from .utils import check_greater_zero, check_between_zero_one

from .utils import compute_pars, s_fun, cd_fun, cl_fun
from .parameters import (
    BattedBallConstants,
    DragForceCoefficients,
    LiftForceCoefficients,
    EnvironmentalParameters,
    UnitConversions,
)


@attr.s(kw_only=True)
class BattedBallTrajectory:
    x0 = attr.ib(default=0, metadata={"units": "ft"})
    y0 = attr.ib(default=2.0, metadata={"units": "ft"})
    z0 = attr.ib(default=3.0, metadata={"units": "ft"})
    spin = attr.ib(default=2675, metadata={"units": "revs_per_second"})
    spin_phi = attr.ib(default=-18.5, metadata={"units": "degrees"})
    drag_strength = attr.ib(default=1, validator=check_between_zero_one)
    magnus_strength = attr.ib(default=1, validator=check_between_zero_one)
    batted_ball_constants = attr.ib(default=BattedBallConstants())

    def __attrs_post_init__(self):
        self.initial_position = np.array((self.x0, self.y0, self.z0))
        self.pi_30 = np.pi / 30

    #  self.initial_position

    def get_trajectory(
        self,
        initial_speed,
        initial_spin,
        launch_angle,
        launch_direction_angle,
        delta_time=0.01,
    ):
        self.pars["launch_angle"] = launch_angle
        self.pars["launch_phi"] = launch_direction_angle
        self.pars = compute_pars(self.pars)

        phi = self.pars["launch_phi"]
        theta = self.pars["launch_angle"]

        self.pars["phi_rad"] = self.pars["launch_phi"] * np.pi / 180
        self.pars["theta_rad"] = self.pars["launch_angle"] * np.pi / 180

        initial_velocity = (
            initial_speed
            * self.pars["mph_to_fts"]
            * np.array(
                [
                    np.cos(self.pars["theta_rad"]) * np.sin(self.pars["phi_rad"]),
                    np.cos(self.pars["theta_rad"]) * np.cos(self.pars["phi_rad"]),
                    np.sin(self.pars["theta_rad"]),
                ]
            )
        )

        rk_solution = RK45(
            self.trajectory_fun,
            0,
            np.concatenate((self.initial_position, initial_velocity), axis=0),
            t_bound=1000,
            max_step=delta_time,
        )
        ans = []
        z = xc[2]
        while z > 0:
            rk_solution.step()
            res = rk_solution.y
            z = res[2]
            ans.append([rk_solution.t] + list(res))
        result_df = pd.DataFrame(np.array(ans).reshape(-1, 7))
        result_df.columns = ["t", "x", "y", "z", "vx", "vy", "vz"]
        return result_df

    def trajectory_fun(self, t, trajectory_vars):
        # trajectory_vars = x, y, z, vx, vy, vz
        _, _, _, vx, vy, vz = trajectory_vars
        v = np.sqrt(vx ** 2 + vy ** 2 + vz ** 2)

        wb = self.pars["backspin"]
        ws = self.pars["sidespin"]

        wx = (
            (
                wb * np.cos(self.pars["phi_rad"])
                - ws * np.sin(self.pars["theta_rad"]) * np.sin(self.pars["phi_rad"])
            )
            * np.pi
            / 30
        )
        wy = (
            (
                -wb * np.sin(self.pars["phi_rad"])
                - ws * np.sin(self.pars["theta_rad"]) * np.cos(self.pars["phi_rad"])
            )
            * np.pi
            / 30
        )
        wz = (ws * np.cos(self.pars["theta_rad"])) * np.pi / 30

        cd = cd_fun(t, v, self.pars)
        cl = cl_fun(t, v, self.pars)
        s = s_fun(t, v, self.pars)

        magnus_const = self.pars["c0"] * cl / self.pars["omega"] * v
        magnus_const = magnus_const * self.pars["magnus_strength"]

        drag_const = self.pars["c0"] * cd * v
        drag_const = self.pars["drag_strength"] * drag_const
        fx = -drag_const * vx + magnus_const * (wy * vz - wz * vy)

        fy = -drag_const * vy + magnus_const * (-wx * vz + wz * vx)

        fz = (
            -drag_const * vz
            + magnus_const * (wx * vy - wy * vx)
            - self.pars["g_gravity"]
        )

        gx = vx
        gy = vy
        gz = vz

        return np.array([gx, gy, gz, fx, fy, fz])
