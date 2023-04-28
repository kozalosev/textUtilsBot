from txtprocutil import collect_help_messages, divide_chunks
from tests.test_txtproc import simple_processors    # import the fixture
from klocmod import LocalizationsContainer


def test_collect_help_messages(simple_processors):
    lang_cont = LocalizationsContainer.from_file("app/localizations.ini")
    messages = collect_help_messages(simple_processors, lang_cont.get_lang('en'))
    assert messages
    msg = messages[0]
    assert msg.name == "binary_encoder"
    assert msg.title and msg.description


def test_divide_chunks():
    assert [[1, 2], [3, 4]] == list(divide_chunks([1, 2, 3, 4], 2))
    assert [[1]] == list(divide_chunks([1], 2))
    assert [] == list(divide_chunks([], 2))
