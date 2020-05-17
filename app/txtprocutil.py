"""
Utility functions related to text processors.

Note, the 'resolve_text_processor_name' function must not be placed in the
'txtproc/util.py' file since that module should know nothing about the
localization system!
"""

from typing import Type, Union
from klocmod import LanguageDictionary

from txtproc import TextProcessor


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
