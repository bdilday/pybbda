from pybaseballdatana.utils import html_table
import pytest


@pytest.mark.parametrize(
    "text, replace_chars, expected",
    [
        ("abc", None, "abc"),
        ("ab/c", None, "ab_c"),
        ("a/b/c", None, "a_b_c"),
        ("a/b/c", "|", "a/b/c"),
        ("a|b|c", "|", "a_b_c"),
    ],
)
def test_replace_chars(text, replace_chars, expected):
    assert html_table.replace_chars(text, replace_chars) == expected


def test_html_table():
    assert True
