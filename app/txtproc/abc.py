"""Abstract base classes that are used throughout the system and by implementers."""

import re
from abc import ABC, abstractmethod

from .util import classproperty


__all__ = ['TextProcessor', 'Exclusive', 'Reversible', 'Universal', 'Encoder', 'Decoder']


class TextProcessor(ABC):
    """
    Base class for all text processors. Your class must extend this one to
    let the loader discover it.

    The key idea is that all processors can answer whether they're able to
    process the string (query) or not. If they can, they must return a
    transformed string when the 'process' method will be invoked.

    Another notable thought that text processors can be exclusive and/or
    reversible. The exclusivity means here that there is the only one processor
    which should handle the query. If such processor is found, the others will
    be discarded. It's mostly useful for decoders.

    The reversibility means, obviously, that the transformed string may be
    transformed back and this reversed transformation has sense. Mostly useful
    for encoders.
    """

    # Marker used instead of 'issubclass' to search for descendants of this class.
    # See: https://stackoverflow.com/a/11461574
    __txtproc__ = True

    is_exclusive = False
    is_reversible = False

    @staticmethod
    @abstractmethod
    def can_process(query: str) -> bool:
        """Return True if the processor can handle the query."""
        pass

    @abstractmethod
    def process(self, query: str) -> str:
        """Transform the query and return the result."""
        pass

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


class Encoder(Universal, Reversible, TextProcessor, ABC):
    """Encoders are reversible text processors that can handle any query."""
    pass


class Decoder(Exclusive, TextProcessor, ABC):
    """Decoders are exclusive processors."""
    pass
