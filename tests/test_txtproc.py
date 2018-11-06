import pytest
from typing import *

import app.strconv as strconv
import app.strconv.binhex64 as binhex64
import app.strconv.langlayout as langlayout
from app.txtproc import TextProcessorsLoader, TextProcessor


@pytest.fixture
def loader() -> TextProcessorsLoader:
    return TextProcessorsLoader(strconv)


@pytest.fixture
def simple_processors() -> Iterable[Type[TextProcessor]]:
    return (
        binhex64.BinaryEncoder,
        binhex64.HexadecimalEncoder,
        binhex64.Base64Encoder,
        langlayout.LanguageLayoutSwitcher,
    )


@pytest.fixture
def exclusive_processors() -> Iterable[Type[TextProcessor]]:
    return (
        binhex64.BinaryDecoder,
        binhex64.HexadecimalDecoder,
        binhex64.Base64Decoder,
    )


def test_import_strconv(loader, simple_processors, exclusive_processors):
    """
    Here I use all current implementations from the 'strconv' module for
    assertions. However, there is no need to append new ones in the future.
    """
    assert all(sp in loader.simple_processors for sp in simple_processors)
    assert all(ep in loader.exclusive_processors for ep in exclusive_processors)


def test_matching_simple_processors(loader, simple_processors, exclusive_processors):
    processor_classes = {type(x) for x in loader.match_simple_processors("hello")}
    assert all(sp in processor_classes for sp in simple_processors)
    assert all(ep not in processor_classes for ep in exclusive_processors)


@pytest.mark.parametrize("query,expected_processor", [
    ('01001000 01100101 01101100 01101100 01101111', binhex64.BinaryDecoder),
    ('48 65 6c 6c 6f 20 57 6f 72 6c 64', binhex64.HexadecimalDecoder),
    ('SGVsbG8gV29ybGQ=', binhex64.Base64Decoder),
])
def test_matching_exclusive_processors(loader, query, expected_processor):
    """
    It may be useful for testing purposes to add more decoders here afterward.
    This can help to ensure that your implementation of the 'can_process' method
    is correct and all processors will match as expected.
    """
    assert type(loader.match_exclusive_processor(query)) is expected_processor


@pytest.mark.parametrize("processor,expected_name", [
    (binhex64.BinaryEncoder, "binary_encoder"),
    (binhex64.HexadecimalDecoder, "hexadecimal_decoder"),
    (langlayout.LanguageLayoutSwitcher, "language_layout_switcher"),
])
def test_name_property(processor, expected_name):
    assert processor.name == processor().name == expected_name
