"""Abstract base classes that are used throughout the system and by implementers."""

import re
from abc import ABC, abstractmethod
from typing import Collection, Optional

from .util import classproperty


__all__ = [
    'TextProcessor', 'PrefixedTextProcessor',
    'Exclusive', 'Reversible', 'Universal', 'HTML',
    'Encoder', 'Decoder'
]


class TextProcessor(ABC):
    """
    Base class for all text processors. Your class must extend this one to
    let the loader discover it.

    The key idea is that all processors can answer whether they're able to
    process the string (query) or not. If they can, they must return a
    transformed string when the 'process' method will be invoked.

    Another notable thought that text processors can be exclusive and/or
    reversible. The exclusivity means here that there is only a subset of
    processors which should handle the query. If such processors are found,
    the others will be discarded. It's mostly useful for decoders.

    The reversibility means, obviously, that the transformed string may be
    transformed back and this reversed transformation has sense. Mostly useful
    for encoders.

    Processors are allowed to return a string containing HTML tags. In this
    case, set the 'use_html' field to True. Note, however, that processors
    must escape HTML entities in the input query by themselves! Use the
    'strconv.util.escape_html' function for that. The parse mode is deliberately
    restricted to HTML only. Telegram flavored Markdown is much harder to
    escape properly.

    If you use HTML, it's likely you'll want to override the 'get_description'
    method as well. By default, description the message equals to its text,
    but Telegram renders all HTML tags inside it as plain text.
    """

    # Marker used instead of 'issubclass' to search for descendants of this class.
    # See: https://stackoverflow.com/a/11461574
    __txtproc__ = True

    is_exclusive = False
    is_reversible = False

    use_html = False

    @classmethod
    @abstractmethod
    def can_process(cls, query: str) -> bool:
        """Return True if the processor can handle the query."""
        pass

    @abstractmethod
    def process(self, query: str, lang_code: str = "") -> str:
        """Transform the query and return the result."""
        pass

    def get_description(self, query: str, lang_code: str = "") -> str:
        """
        By default, description of the message equals to the processed text itself.
        This method allows subclasses to override this behavior.
        """
        return self.process(query, lang_code)

    @classproperty
    @classmethod
    def name(cls) -> str:
        """Return the name of the class."""
        return cls.__name__

    @classproperty
    @classmethod
    def snake_case_name(cls) -> str:
        """
        Return the name of the class in snake_case.

        May be useful to use this string as a key for localization dictionary,
        for example.
        """
        def to_snake_case(name):
            """https://stackoverflow.com/a/1176023"""
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

        return to_snake_case(cls.__name__)


class PrefixedTextProcessor(TextProcessor, ABC):
    """
    Base class for text processors that's not used by default, only when text
    starts with some prefix(-es), like this: "{prefix}: {text}". Perfectly fits
    for URL addresses (they start with "http://" or "https://").

    Instead of defining methods 'can_process' and 'process' you must define
    methods 'get_prefixes', that returns (obviously) a collection of prefixes,
    and 'transform', that takes the text (with or without prefix, depends on the
    `should_strip_prefix` class variable).
    """
    should_strip_prefix = False

    @classmethod
    @abstractmethod
    def get_prefixes(cls) -> Collection[str]:
        """A collection of prefixes."""
        pass

    @abstractmethod
    def transform(self, text: str) -> str:
        """
        This method has the same meaning as the 'process' method for usual text
        processors, but it takes the text with prefix cut off (if variable
        `should_strip_prefix` is True).
        """
        pass

    @classmethod
    @abstractmethod
    def text_filter(cls, text: str) -> bool:
        """
        Override this method instead of `can_process()` to determine if the
        processor can handle the query.

        :param text: the query with prefix stripped off (or not if `should_strip_prefix` is False)
        :return: True if the processor can handle the query
        """
        pass

    @classmethod
    def _prepare(cls, query: str, prefix: Optional[str] = None) -> str:
        """
        Prepares the query to handle by a processor.

        The behavior of this method depends on the `should_strip_prefix` class
        variable. If it's True, the prefix will be cut off. If it's False,
        the query will be passed as-is.

        :param query: a text query to prepare
        :param prefix: if the prefix is already known, pass it here to prevent double computation
        """
        if not cls.should_strip_prefix:
            return query

        if prefix is None:
            prefix = next(p for p in cls.get_prefixes() if query.startswith(p))
        return query[len(prefix):].lstrip()

    @classmethod
    def can_process(cls, query: str) -> bool:
        return any(query.startswith(p) and cls.text_filter(cls._prepare(query, p)) for p in cls.get_prefixes())

    def process(self, query: str, lang_code: str = "") -> str:
        return self.transform(self._prepare(query))


class Exclusive:
    """Mix-in class that sets exclusivity."""
    is_exclusive = True


class Reversible:
    """Mix-in class that sets reversibility."""
    is_reversible = True


class Universal:
    """Mix-in class that's used for processors that can handle any text."""
    @classmethod
    def can_process(cls, _: str) -> bool:
        return True


class HTML:
    """Mix-in class that enables the use of HTML tags."""
    use_html = True


# Shortcuts for common cases

class Encoder(Reversible, TextProcessor, ABC):
    """Encoders are reversible text processors."""
    pass


class Decoder(Exclusive, TextProcessor, ABC):
    """Decoders are exclusive processors."""
    pass
