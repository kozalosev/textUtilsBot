class ExternalServiceError(Exception):
    pass


class UnsupportedCurrency(Exception):
    def __init__(self, *curr: str) -> None:
        self.currencies = list(curr)

    def __str__(self) -> str:
        return f"UnsupportedCurrency{self.currencies}"


class UnknownLanguageCode(Exception):
    def __init__(self, lang_code: str) -> None:
        self.lang_code = lang_code

    def __str__(self) -> str:
        return f"UnknownLanguageCode({self.lang_code})"
