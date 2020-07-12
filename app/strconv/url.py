"""
URL encoder and decoder.

These text processors work only for URL addresses that start with "http://" or "https://".
"""

import re
from abc import ABC
from typing import Collection
from urllib.parse import quote, unquote, urlparse, urlunparse

from txtproc.abc import PrefixedTextProcessor, Reversible


_re_url_encoded_char = re.compile("%[0-9]{2}")


class URLPrefixedTextProcessor(PrefixedTextProcessor, ABC):
    @classmethod
    def get_prefixes(cls) -> Collection[str]:
        return {"http://", "https://"}


class URLEncoder(Reversible, URLPrefixedTextProcessor):
    @classmethod
    def text_filter(cls, text: str) -> bool:
        return "xn--" not in text and _re_url_encoded_char.search(text) is None

    def transform(self, text: str) -> str:
        url_address = urlparse(text)
        encoded_url_address = (
            url_address.scheme,
            self._process_netloc(url_address.netloc),
            quote(url_address.path),
            quote(url_address.params, safe=";="),
            quote(url_address.query, safe="&="),
            quote(url_address.fragment)
        )
        return urlunparse(encoded_url_address)

    @staticmethod
    def _process_netloc(domains: str) -> str:
        encoded_domains = [domain.encode('idna').decode('utf-8') for domain in domains.split('.')]
        return '.'.join(encoded_domains)


class URLDecoder(URLPrefixedTextProcessor):
    @classmethod
    def text_filter(cls, text: str) -> bool:
        return ("xn--" in text or _re_url_encoded_char.search(text) is not None) and cls.do_transform(text) != text

    # We need to call the execution of transformation from a class-level method.
    # Because of that, we have 2 following methods:
    def transform(self, text: str) -> str:
        return self.do_transform(text)

    @classmethod
    def do_transform(cls, text: str) -> str:
        url_address = urlparse(text)

        decoded_netloc = url_address.netloc
        try:
            decoded_netloc = cls._process_netloc(url_address.netloc)
        except UnicodeDecodeError:
            # I don't want to log all this garbage
            pass

        decoded_url_address = (
            url_address.scheme,
            decoded_netloc,
            unquote(url_address.path),
            unquote(url_address.params),
            unquote(url_address.query),
            unquote(url_address.fragment)
        )
        return urlunparse(decoded_url_address)

    @staticmethod
    def _process_netloc(domains: str) -> str:
        decoded_domains = [domain.encode('utf-8').decode('idna') for domain in domains.split('.')]
        return '.'.join(decoded_domains)
