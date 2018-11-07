import pytest
from strconv.typographer import TypographerConverter


@pytest.fixture
def converter() -> TypographerConverter:
    return TypographerConverter()


def test_matcher(converter):
    assert not converter.can_process("hello world")
    assert converter.can_process('Leonid "SadBot" Kozarin')
    assert converter.can_process("(C) Kozalo.Ru")
    assert converter.can_process("Kozalo(тм)")
    assert converter.can_process("(r)")


def test_converter(converter):
    assert converter.process('Leonid "SadBot" Kozarin') == "Leonid «SadBot» Kozarin"
    assert converter.process("(C) Kozalo.Ru") == "© Kozalo.Ru"
    assert converter.process("Kozalo(тм)") == "Kozalo™"    # just for testing purposes, there is no actual registration
    assert converter.process("(r)") == "®"
