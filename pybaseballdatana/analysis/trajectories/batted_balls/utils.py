import numpy as np


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


def compute_pars(pars):
    pars["elevation_m"] = pars["elevation_ft"] * pars["ft_to_m"]
    pars["temperature_c"] = (pars["temperature_f"] - 32) * 5 / 9
    pars["pressure_mm_hg"] = pars["pressure_in_hg"] * 1000 / 39.37
    pars["RH"] = pars["relative_humidity"]
    pars["SVP"] = 4.5841 * np.exp(
        (18.687 - pars["temperature_c"] / 234.5)
        * pars["temperature_c"]
        / (257.14 + pars["temperature_c"])
    )

    pars["rho"] = 1.2929 * (
        273
        / (pars["temperature_c"] + 273)
        * (
            pars["pressure_mm_hg"] * np.exp(-pars["beta"] * pars["elevation_m"])
            - 0.3783 * pars["RH"] * pars["SVP"] * 0.01
        )
        / 760
    )

    pars["c0"] = (
        0.07182
        * pars["rho"]
        * pars["kgm3_to_lbft3"]
        * (5.125 / pars["mass"])
        * (pars["circumference"] / 9.125) ** 2
    )

    pars["sidespin"] = pars["spin"] * np.sin(pars["spin_phi"] * np.pi / 180)
    pars["backspin"] = pars["spin"] * np.cos(pars["spin_phi"] * np.pi / 180)
    pars["omega"] = pars["spin"] * np.pi / 30
    pars["romega"] = pars["circumference"] * pars["omega"] / (24 * np.pi)

    return pars


def s_fun(t, vw, pars):
    return (pars["romega"] / vw) * np.exp(-t * vw / (pars["tau"] * 146.7))


def cl_fun(t, vw, pars):
    s = s_fun(t, vw, pars)
    return pars["cl2"] * s / (pars["cl0"] + pars["cl1"] * s)


def cd_fun(t, vw, pars):
    return pars["cd0"] + pars["cdspin"] * (pars["spin"] * 1e-3) * np.exp(
        -t * vw / (pars["tau"] * 146.7)
    )
