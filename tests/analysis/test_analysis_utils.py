from pybbda.analysis.utils import check_len
import pytest


def test_check_len():
    check_len(None, "some", (0, 1, 2), 3)

    with pytest.raises(ValueError):
        check_len(None, "some", (0, 1, 2), 4)
