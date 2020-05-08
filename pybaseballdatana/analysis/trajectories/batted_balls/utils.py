import numpy as np
from functools import partial


def _trig_in_degrees(trig_func, angle_in_degrees):
    return trig_func(np.deg2rad(angle_in_degrees))


cos_in_degrees = partial(_trig_in_degrees, np.cos)
sin_in_degrees = partial(_trig_in_degrees, np.sin)


def check_greater_zero(instance, attribute, value):
    if value <= 0:
        raise ValueError(
            "{} must be greater than zero, not {}".format(attribute, value)
        )


def check_between_zero_one(instance, attribute, value):
    if not 0 <= value <= 1:
        raise ValueError(
            "{} must be between zero and one, not {}".format(attribute, value)
        )

