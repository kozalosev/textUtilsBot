from queryutil import *


def test_answers():
    s = InlineQueryResultsBuilder().add(
        type='foo',
        test=True,
    ).add(
        type='bar',
        test=0,
        result_id='foo'
    )
    e = [
        {'type': 'foo', 'id': '0', 'test': True},
        {'type': 'bar', 'id': '1:foo', 'test': 0}
    ]
    assert s.build_list() == e


def test_add_article_to():
    a = InlineQueryResultsBuilder()
    add_article = get_articles_generator_for(a, max_description=10)
    add_article("foo", "test 1")
    add_article("bar", "test long string")
    add_article("baz", "<b>test 3</b>", description="test 3", parse_mode="HTML", article_id="foo")
    e = [{
        'type': 'article',
        'id': '0',
        'title': 'foo',
        'description': 'test 1',
        'input_message_content': {
            'message_text': 'test 1',
            'parse_mode': ""
        }
    }, {
        'type': 'article',
        'id': '1',
        'title': 'bar',
        'description': 'test long…',
        'input_message_content': {
            'message_text': 'test long string',
            'parse_mode': ""
        }
    }, {
        'type': 'article',
        'id': '2:foo',
        'title': 'baz',
        'description': 'test 3',
        'input_message_content': {
            'message_text': '<b>test 3</b>',
            'parse_mode': "HTML"
        }
    }]
    assert a.build_list() == e
