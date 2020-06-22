import numpy as np
from functools import partial


def _trig_in_degrees(trig_func, angle_in_degrees):
    return trig_func(np.deg2rad(angle_in_degrees))


cos_in_degrees = partial(_trig_in_degrees, np.cos)
sin_in_degrees = partial(_trig_in_degrees, np.sin)


def check_is_zero_one(instance, attribute, value):
    if value not in [0, 1]:
        raise ValueError("{} must be either 0 or 1, not {}".format(attribute, value))


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


def check_len(instance, attribute, value, len_constraint=-1):
    if len(value) != len_constraint:
        raise ValueError(
            "length of {} must be {}, not {}".format(
                attribute, len_constraint, len(value)
            )
        )
