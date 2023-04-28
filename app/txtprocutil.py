"""
Utility functions related to text processors.

Note, the 'resolve_text_processor_name' function must not be placed in the
'txtproc/util.py' file since that module should know nothing about the
localization system!
"""

from dataclasses import dataclass
from typing import Type, Union, Iterable, List, TypeVar, Collection, FrozenSet
from klocmod import LanguageDictionary

from txtproc import TextProcessor

T = TypeVar('T')


def resolve_text_processor_name(processor: Union[Type[TextProcessor], TextProcessor], lang: LanguageDictionary) -> str:
    """
    Resolve the human-readable name of a text processor.

    Try to retrieve the name of the text processor from the localization system
    first. If the attempt was unsuccessful, return the name of the text
    processor class.

    :param processor: a text processor which name we need to know
    :param lang: a language dictionary from the localization system
    :return: the human-readable name of a text processor
    """
    key = 'hint_' + processor.snake_case_name
    localized_processor_name = lang[key]
    if localized_processor_name == key:
        return processor.name
    return localized_processor_name


@dataclass
class TextProcessorHelp:
    name: str
    title: str
    description: str


def collect_help_messages(processors: FrozenSet[Type[TextProcessor]],
                          lang: LanguageDictionary) -> List[TextProcessorHelp]:
    """Collects help information about text processors in a more convenient representation."""
    res = []
    for processor in processors:
        proc_name = processor.snake_case_name
        help_message_key = 'help_' + proc_name
        localized_help_message = lang[help_message_key]
        # skip empty and undefined help messages
        if len(localized_help_message.strip()) == 0 or localized_help_message == help_message_key:
            continue
        localized_processor_name = resolve_text_processor_name(processor, lang)
        res.append(TextProcessorHelp(proc_name, localized_processor_name, localized_help_message))
    return res


def divide_chunks(lst: Collection[T], n: int) -> Iterable[Collection[T]]:
    """Split a list to a list of lists of n elements."""
    lst = list(lst)
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
