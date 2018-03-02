"""Utility functions for string conversions."""

import re
from typing import Optional


__all__ = ['escape_html', 'str_to_bin', 'str_to_hex', 'bin_to_str', 'hex_to_str']


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


def str_to_bin(s: str) -> str:
    """
    'Hello' => '01001000 01100101 01101100 01101100 01101111'
    """
    b = s.encode()
    str_bytes = ["{:08b}".format(n) for n in b]
    return " ".join(str_bytes)


def str_to_hex(s: str) -> str:
    """
    'Hello World' => '48 65 6c 6c 6f 20 57 6f 72 6c 64'
    """
    h = s.encode().hex()
    bl = split_every_n_characters(2, h)
    return " ".join(bl)


def bin_to_str(b: str) -> Optional[str]:
    """
    '01001000 01100101 01101100 01101100 01101111' => 'Hello'
    """
    b = re.sub("\s+", "", b)
    str_bytes = split_every_n_characters(8, b)
    try:
        numbers = [int(b, 2) for b in str_bytes]
    except ValueError:
        return None
    nb = bytes(numbers)
    try:
        chars = nb.decode()
    except UnicodeDecodeError:
        return None
    return "".join(chars)


def hex_to_str(s: str) -> Optional[str]:
    """
    '48 65 6c 6c 6f 20 57 6f 72 6c 64' => 'Hello World'
    """
    try:
        return bytearray.fromhex(s).decode()
    except ValueError:
        return None
