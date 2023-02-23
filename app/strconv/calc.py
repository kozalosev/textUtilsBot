"""Embedded calculator and currency exchanger for the bot."""

import re
import logging
from io import StringIO
from txtproc.abc import TextProcessor
from strconv import currates

_subst_re = re.compile(r"\{\{(?P<expr>[0-9+\-*/%^., ]+?) *?"
                       r"((?P<from_curr>[A-Z]{3,}|[$€₽£¥]) *?"
                       r"(to|>) *?"
                       r"(?P<to_curr>[A-Z]{3,}|[$€₽£¥]))?? *?}}")
_logger = logging.getLogger(__file__)
_MAX_RECURSION = 100

try:
    # noinspection PyPackageRequirements
    import numexpr

    def numexpr_eval(s):
        return numexpr.evaluate(s).take(0)
    _eval_func = numexpr_eval
    _logger.info("numexpr eval is used")
except ModuleNotFoundError:
    _eval_func = eval
    _logger.info("unsafe eval is used")


class Calculator(TextProcessor):
    _logger = logging.getLogger(__name__)

    @classmethod
    def can_process(cls, query: str) -> bool:
        return bool(_subst_re.search(query))

    def process(self, query: str, lang_code: str = "") -> str:
        try:
            return self.next_expr(query, lang_code, StringIO())
        except currates.ExternalServiceError as err:
            self._logger.error(err)
            return ""   # the bot will ignore this result
        except currates.UnsupportedCurrency as err:
            self._logger.warning(f"The following currency was requested but is not present in our data: {err}")
            return ""   # the bot will ignore this result

    def next_expr(self, query: str, lang_code: str, sb: StringIO, pos: int = 0, guard: int = 0) -> str:
        match = _subst_re.search(query, pos=pos)
        if not match or self._check_guard(guard, query):
            sb.write(query[pos:])
            return sb.getvalue()
        sb.write(query[pos:match.start()])
        val = _eval_func(match.group("expr").strip())
        from_curr = match.group("from_curr")
        to_curr = match.group("to_curr")
        if from_curr and to_curr:
            val = currates.convert(from_curr, to_curr, val, lang_code)
            val = self._format_number(val)
            if len(to_curr) == 1:
                sb.write(f"{to_curr}{val}")
            else:
                sb.write(f"{val} {to_curr}")
        else:
            sb.write(self._format_number(val))
        return self.next_expr(query, lang_code, sb, match.end(), guard+1)

    def _check_guard(self, guard: int, query: str) -> bool:
        if guard >= _MAX_RECURSION:
            self._logger.warning("Maximum level of recursions was reached while evaluating: " + query)
            return True
        return False

    @staticmethod
    def _format_number(val: float) -> str:
        """3.1415 => 3.14 but 3.00 => 3"""
        val_int = int(val)
        return f"{val:.2f}" if val % val_int != 0 else str(val_int)
