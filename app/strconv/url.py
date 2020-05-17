"""
URL encoder and decoder.

These text processors work only for strings that start with prefix "url:".
"""

import re
from abc import ABC
from urllib.parse import quote, unquote

from txtproc.abc import PrefixedTextProcessor


class URLPrefixedTextProcessor(PrefixedTextProcessor, ABC):
    @classmethod
    def get_prefix(cls) -> str:
        return "url"


class URLEncoder(URLPrefixedTextProcessor):
    def transform(self, text: str) -> str:
        return quote(text)


class URLDecoder(URLPrefixedTextProcessor):
    re_encoded_char = re.compile("%[0-9]{2}")

    @classmethod
    def can_process(cls, query: str) -> bool:
        return super().can_process(query) and cls.re_encoded_char.search(query)

    def transform(self, text: str) -> str:
        return unquote(text)
