import re
from txtproc.abc import TextProcessor


class TypographerConverter(TextProcessor):
    replacements = [
        ("<<", "«"),
        (">>", "»"),
        ("--", "—"),
        ("\.{3}", "…"),
        ("!=", "≠"),
        ("~=", "≈"),
        ("<=", "≤"),
        (">=", "≥"),
        ("<-", "←"),
        ("->", "→"),
        (r"\([cс]\)", "©"),
        (r"\(r\)", "®"),
        (r"\([tт][mм]\)", "™"),
    ]

    @classmethod
    def can_process(cls, query: str):
        patterns = (pattern for pattern, replacement in cls.replacements)
        return any(re.search(pattern, query, flags=re.IGNORECASE) for pattern in patterns)

    def process(self, query: str, lang_code: str = "") -> str:
        result = query
        for pattern, replacement in self.replacements:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        return result
