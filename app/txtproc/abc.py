"""Abstract base classes that are used throughout the system and by implementers."""

import re
from abc import ABC, abstractmethod

from .util import classproperty


__all__ = ['TextProcessor', 'Exclusive', 'Reversible', 'Universal', 'HTML', 'Encoder', 'Decoder']


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
    def process(self, query: str) -> str:
        """Transform the query and return the result."""
        pass

    def get_description(self, query: str) -> str:
        """
        By default, description of the message equals to the processed text itself.
        This method allows subclasses to override this behavior.
        """
        return self.process(query)

    @classproperty
    @classmethod
    def name(cls) -> str:
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


class Exclusive:
    """Mix-in class that sets exclusivity."""
    is_exclusive = True


class Reversible:
    """Mix-in class that sets reversibility."""
    is_reversible = True


class Universal:
    """Mix-in class that's used for processors that can handle any text."""
    @staticmethod
    def can_process(_: str) -> bool:
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
