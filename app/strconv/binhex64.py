"""
Binary/hexadecimal/base64 encoders and decoders.

Mostly this module is just a wrapper over functions form the
'strconv.util.binhex64' module. Such approach simplifies the testing and
allows us to use actual functions returning 'Optional' results for both
checking of ability to handle the query and actual processing.
"""

import string

from txtproc.abc import Encoder, Decoder
from .util.binhex64 import *


class BinaryEncoder(Encoder):
    def process(self, query: str) -> str:
        return str_to_bin(query)


class BinaryDecoder(Decoder):
    @staticmethod
    def can_process(query: str) -> bool:
        return all(char in ('0', '1', ' ') for char in query) and bin_to_str(query)

    def process(self, query: str) -> str:
        return bin_to_str(query)


class HexadecimalEncoder(Encoder):
    def process(self, query: str) -> str:
        return str_to_hex(query)


class HexadecimalDecoder(Decoder):
    @staticmethod
    def can_process(query: str) -> bool:
        # Since this processor is able to handle the same queries the BinaryDecoder can, we need to ensure that
        # we won't swallow binary strings here.
        if BinaryDecoder.can_process(query):
            return False
        return all(char in string.hexdigits + ' ' for char in query) and hex_to_str(query)

    def process(self, query: str) -> str:
        return hex_to_str(query)


class Base64Encoder(Encoder):
    def process(self, query: str) -> str:
        return str_to_base64(query)


class Base64Decoder(Decoder):
    @staticmethod
    def can_process(query: str) -> bool:
        return all(char in string.ascii_letters + string.digits + '+/=' for char in query) and base64_to_str(query)

    def process(self, query: str) -> str:
        return base64_to_str(query)
