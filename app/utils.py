from typing import TypeVar, Generic, Callable, Optional

T = TypeVar('T')


class Lazy(Generic[T]):
    """Lazily-initialized transparent proxy (single-threaded asyncio context).

    Double-underscore attributes (__factory, __value) trigger Python name mangling
    (_Lazy__factory, _Lazy__value), so they live in __dict__ and are found before
    __getattr__ is ever called — no recursion risk.
    """

    def __init__(self, factory: Callable[[], T]):
        self.__factory = factory
        self.__value: Optional[T] = None

    def _unwrap(self) -> T:
        if self.__value is None:
            self.__value = self.__factory()
        return self.__value

    # Transparent forwarding of regular attribute/method access (.execute(), .commit(), .close(), etc.)
    def __getattr__(self, name: str):
        return getattr(self._unwrap(), name)

    # Special methods for dbm-like objects (Python looks these up on the type, not via __getattr__)
    def __getitem__(self, key):        return self._unwrap()[key]
    def __setitem__(self, key, value): self._unwrap()[key] = value
    def __contains__(self, key):       return key in self._unwrap()
    def __len__(self):                 return len(self._unwrap())

    def _set_for_testing(self, value: T) -> None:
        """Replace the underlying value. For use in tests only."""
        self.__value = value
