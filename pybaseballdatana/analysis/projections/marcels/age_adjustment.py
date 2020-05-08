from pandas import isnull


def age_adjustment(age):
    """

    :param age:
    :return:
    """
    if isnull(age):
        return float("nan")
    elif age <= 0:
        return 1
    elif age >= 29:
        return 1 / (1 + 0.003 * (age - 29))
    elif age < 29:
        return 1 + 0.006 * (29 - age)
