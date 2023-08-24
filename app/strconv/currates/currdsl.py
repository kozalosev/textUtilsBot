"""
Domain specific language to define mappings from natural languages into currency codes.
:see: ../../data/currates_conf.py
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple


class CurrABC(ABC):
    @abstractmethod
    def matches(self, s: str) -> bool:
        """:returns: True if 's' matches against the currency defined by an instance of an implementation of this ABC"""
        pass

    @abstractmethod
    def resolve_declension(self, num: float) -> str:
        """:returns: the right declension for the value of a 'num'"""
        pass


class Words(CurrABC, ABC):
    """Abstract base class for names of currencies in natural languages."""
    pass


class InEnglish(Words):
    """Implementation (very simplified) for English words (singular and plural forms)."""

    def __init__(self, singular: str) -> None:
        self._singular = singular
        self._plural = singular + "s"

    def matches(self, s: str) -> bool:
        return s in [self._singular, self._plural]

    def resolve_declension(self, num: float) -> str:
        return self._singular if num == 1 else self._plural


class InRussian(Words):
    """Implementation for Russian words (declensions and singular and plural forms)."""

    def __init__(self, head: str, tails: Optional[Tuple[str, str, str]] = None) -> None:
        """
        :param head: the root of a currency name word
        :param tails: 3 endings: for 1, 2 and 5
        """
        self._head = head
        self._tails = tails

    def matches(self, s: str) -> bool:
        lh = len(self._head)
        return len(s) >= lh and s[:lh] == self._head

    def resolve_declension(self, num: float) -> str:
        if not self._tails:
            return self._head
        match num % 10:
            case 1 if num != 11: return self._head + self._tails[0]
            case 2 | 3 | 4 if num not in [12, 13, 14]: return self._head + self._tails[1]
            case _: return self._head + self._tails[2]


class Currency(CurrABC):
    """
    The main class to define a mapping.
    :see: ../../data/currates_conf.py
    """

    def __init__(self, code: str, *signs: str, words: List[Words] = ()) -> None:
        """
        Use this constructor only for describing a currency in the config file!

        To use other methods, this instance must be cloned via the `clone()` method!
        Another option is to create an instance from a code by using the `from_code()` class method!

        :param code: like USD, RUB, BTC, ETH, WAVES, etc.
        :param signs: like $, ₽, руб., etc.
        :param words: instances of the `Words` subclasses
        """
        self._signs = signs
        self._code = code.upper()
        self._words = words

        self._s: Optional[str] = None
        self._matched_words: Optional[CurrABC] = None

        # flag to fail fast in other methods if this constructor was used not for describing
        self._abstract = True

    @classmethod
    def from_code(cls, code: str) -> 'Currency':
        """:returns: a non-abstract instance of the currency from its code"""
        instance = cls(code.upper())
        instance._abstract = False
        return instance

    def matches(self, s: str) -> bool:
        assert not self._abstract

        if s == self._code or s in self._signs:
            self._s = s
            return True
        self._matched_words = next((w for w in self._words if w.matches(s)), None)
        return self._matched_words is not None

    def resolve_declension(self, num: float) -> str:
        assert not self._abstract

        if self._matched_words:
            return self._matched_words.resolve_declension(num)
        elif self._s:
            return self._s
        else:
            return self._code

    @property
    def code(self) -> str:
        return self._code

    def clone(self) -> 'Currency':
        """:returns: a non-abstract clone of the currency"""
        instance = self.__class__(self._code, *self._signs, words=self._words)
        instance._abstract = False
        return instance
