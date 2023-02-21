"""L E T ' S   M A K E   B A N N E R S ! ! !"""

from io import StringIO

from txtproc.abc import Universal, HTML, TextProcessor
from .util import escape_html


def spaced_text(text: str) -> str:
    def spaced_text_generator(s: str):
        for c in s:
            yield c
            yield ' '

    new_str = StringIO()
    for ch in spaced_text_generator(text):
        new_str.write(ch)
    return new_str.getvalue().rstrip()


class BannerMaker(Universal, HTML, TextProcessor):
    def process(self, query: str, lang_code: str = "") -> str:
        banner = spaced_text(escape_html(query)).upper()
        return "<code>{}</code>".format(banner)

    def get_description(self, query: str, lang_code: str = "") -> str:
        return spaced_text(query).upper()
