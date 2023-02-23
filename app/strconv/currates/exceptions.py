class ExternalServiceError(Exception):
    pass


class UnsupportedCurrency(Exception):
    def __init__(self, *curr: str) -> None:
        self.currencies = list(curr)

    def __str__(self) -> str:
        return f"UnsupportedCurrency{self.currencies}"
