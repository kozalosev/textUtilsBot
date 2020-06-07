"""
URL encoder and decoder.

These text processors work only for strings that start with prefix "url:".
"""

import re
from abc import ABC
from urllib.parse import quote, unquote

from txtproc.abc import PrefixedTextProcessor


_re_url_encoded_char = re.compile("%[0-9]{2}")


class URLPrefixedTextProcessor(PrefixedTextProcessor, ABC):
    @classmethod
    def get_prefix(cls) -> str:
        return "url"


class URLEncoder(URLPrefixedTextProcessor):
    @classmethod
    def text_filter(cls, text: str) -> bool:
        return _re_url_encoded_char.search(text) is None

    def transform(self, text: str) -> str:
        return quote(text)


class URLDecoder(URLPrefixedTextProcessor):
    @classmethod
    def text_filter(cls, text: str) -> bool:
        return _re_url_encoded_char.search(text) is not None

    def transform(self, text: str) -> str:
        return unquote(text)


class PunycodeEncoder(URLPrefixedTextProcessor):
    @classmethod
    def text_filter(cls, text: str) -> bool:
        return not text.startswith("xn--")

    def transform(self, text: str) -> str:
        return text.encode('idna').decode('utf-8')


class PunycodeDecoder(URLPrefixedTextProcessor):
    @classmethod
    def text_filter(cls, text: str) -> bool:
        if not text.startswith("xn--"):
            return False
        try:
            cls._decode(text)
        except UnicodeDecodeError:
            return False
        return True

    def transform(self, text: str) -> str:
        return self._decode(text)

    @classmethod
    def _decode(cls, s: str) -> str:
        return s.encode('utf-8').decode('idna')
