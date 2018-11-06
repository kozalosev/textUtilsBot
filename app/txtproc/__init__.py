"""
System for automatic dynamic loading of text processors.

It automatically loads all non-abstract implementations of the 'TextProcessor'
class from some module or a whole package. Just use the 'TextProcessorLoader'
class.

If you're a developer of a new text processor, see the 'abc' module.
"""

from .loader import TextProcessorsLoader
from .abc import TextProcessor
