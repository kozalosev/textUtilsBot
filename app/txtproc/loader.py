import inspect
import pkgutil
import importlib
from typing import *

from .abc import TextProcessor

T = TypeVar('T')
TextProcessorTypesPair = Tuple[Type[TextProcessor], Type[TextProcessor]]
TextProcessorsPair = Tuple[TextProcessor, TextProcessor]


def get_implementations_from_module(cls: Type[T], module) -> Iterable[Type[T]]:
    """
    Scan the module and return a list of non-abstract implementations of
    the abstract 'cls' class.
    """
    assert inspect.isabstract(cls)

    def only_non_abstract_subclasses(obj):
        return inspect.isclass(obj) and hasattr(obj, '__txtproc__') and not inspect.isabstract(obj)
    classes = inspect.getmembers(module, only_non_abstract_subclasses)
    return [class_object for name, class_object in classes]


def get_implementations_from_package(cls: Type[T], package) -> Iterable[Type[T]]:
    """Call 'get_implementations_from_module' for all modules in the package."""
    assert hasattr(package, '__path__')

    module_names = (t[1] for t in pkgutil.iter_modules(package.__path__) if not t[2])
    module_full_names = ("{}.{}".format(package.__name__, name) for name in module_names)
    modules = (importlib.import_module(name) for name in module_full_names)
    impls = (get_implementations_from_module(cls, module) for module in modules)
    return (x for module_impls in impls for x in module_impls)


def get_implementations(cls: Type[T], obj) -> Iterable[Type[T]]:
    """Shortcut that determines whether 'obj' is a module or package automatically."""
    if hasattr(obj, '__path__'):
        return get_implementations_from_package(cls, obj)
    else:
        return get_implementations_from_module(cls, obj)


class TextProcessorsLoader:
    """
    Container of text processors, that is intended for end users. Depending of
    the constructor parameter, it gathers all concrete implementations of
    the 'TextProcessor' class from either a module or all modules in some
    package.
    """
    all_processors = None          # type: FrozenSet[Type[TextProcessor]]
    exclusive_processors = None    # type: Iterable[Type[TextProcessor]]
    simple_processors = None       # type: Iterable[Type[TextProcessor]]

    def __init__(self, module_or_package):
        impls = set(get_implementations(TextProcessor, module_or_package))
        self.all_processors = frozenset(impls)
        self.exclusive_processors = {x for x in impls if x.is_exclusive}
        self.simple_processors = {x for x in impls if x not in self.exclusive_processors}

    def match_exclusive_processors(self, query: str, lang_code: str = "") -> Iterable[TextProcessor]:
        """
        Iterate over the list of exclusive processors. Returns the list of
        instances of all processors which can process the query.
        """
        return [x() for x in self.exclusive_processors if x.can_process(query, lang_code)]

    def match_simple_processors(self, query: str, lang_code: str = "") -> Iterable[TextProcessor]:
        """
        Iterate over the list of non-exclusive processors. Returns the list of
        instances of all processors which can process the query.
        """
        return [x() for x in self.simple_processors if x.can_process(query, lang_code)]
