"""Utility functions for string conversions."""


def escape_html(text: str) -> str:
    """Replaces all angle brackets with HTML entities."""
    return text.replace('<', '&lt;').replace('>', '&gt;')


def split_every_n_characters(n: int, s: str) -> list:
    """Split a string every `n` characters.
    :param n: the number that determines the length of output strings
    :param s: any string
    :return: a list of strings where all of them are `n` characters long (except the last one)
    :link: https://stackoverflow.com/a/9475354
    """
    return [s[i:i+n] for i in range(0, len(s), n)]
