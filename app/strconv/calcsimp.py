"""Simplified variant of `.calc.Calculator` working with only one expression."""

import re

from txtproc.abc import TextProcessor
from . import currates
from .calc import Calculator

_subst_re = re.compile(r"^(?P<expr>[0-9+\-*/%^., ()]+?)? *?"
                       r"((?P<from_curr>[A-Za-zа-я]{3,}|[$€₽£¥]) *?"
                       r"(to|>|в)? *?"
                       r"(?P<to_curr>[A-Za-zа-я]{3,}|[$€₽£¥])?)??$")


class SingleExpressionCalculator(TextProcessor):
    _calc = Calculator()

    @classmethod
    def can_process(cls, query: str, lang_code: str = "") -> bool:
        if len(query) == 0:
            return False
        match = _subst_re.search(query)
        if not match:
            return False
        from_curr = match.group("from_curr")
        to_curr = match.group("to_curr")
        if from_curr is None:
            return True
        return currates.currency_exists(from_curr, lang_code) and \
            (to_curr is None or currates.currency_exists(to_curr, lang_code))

    def process(self, query: str, lang_code: str = "") -> str:
        expr = _subst_re.search(query).group("expr")
        if not expr:
            query = "1 " + query
        return self._calc.process("{{" + query + "}}", lang_code)
