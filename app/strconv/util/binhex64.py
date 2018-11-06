"""Functions for binary/hexadecimal/base64 conversions."""

import re
import base64
import binascii
from typing import Optional

from . import split_every_n_characters


__all__ = ['str_to_bin', 'str_to_hex', 'str_to_base64',
           'bin_to_str', 'hex_to_str', 'base64_to_str']


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


def str_to_base64(s: str) -> str:
    """
    'Hello World' => 'SGVsbG8gV29ybGQ='
    """
    return base64.b64encode(bytes(s, 'UTF-8')).decode('UTF-8')


def bin_to_str(b: str) -> Optional[str]:
    """
    '01001000 01100101 01101100 01101100 01101111' => 'Hello'
    'usual text' => None
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
    'usual text' => None
    """
    try:
        return bytearray.fromhex(s).decode()
    except ValueError:
        return None


def base64_to_str(b: str) -> Optional[str]:
    """
    'SGVsbG8gV29ybGQ=' => 'Hello World'
    'usual text' => None
    """
    try:
        return base64.b64decode(bytes(b, 'UTF-8')).decode('UTF-8')
    except (binascii.Error, UnicodeDecodeError):
        return None
