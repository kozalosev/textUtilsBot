"""Utilities to make composing of inline query results easier."""

import logging


class InlineQueryResultsBuilder:
    """A helper class to make the creation of a result to an inline query a bit easier.
    It takes responsibility for setting proper `id`s to your `InlineQueryResult`s
    """

    _logger = logging.getLogger(__name__)

    def __init__(self):
        self._id = 0
        self._list = []

    # noinspection PyShadowingBuiltins
    def add(self, type: str, **kwargs) -> "InlineQueryResultsBuilder":
        """Append a new result to the internal list. Can be used in chains of methods.
        :param type: see https://core.telegram.org/bots/api#inlinequeryresult
        """
        obj = kwargs
        obj['type'] = type
        obj['id'] = str(self._id)
        self._id += 1
        self._list.append(obj)
        return self

    def build_list(self) -> list:
        """:return: a copy of the internal list with non-empty results"""
        def non_empty_message(x) -> bool:
            return 'input_message_content' not in x or len(x['input_message_content']['message_text']) > 0
        valid_msgs = [x for x in self._list if non_empty_message(x)]
        if len(valid_msgs) != len(self._list):
            invalid_msgs = [x for x in self._list if not non_empty_message(x)]
            self._logger.warning(f"Some empty inline results were filtered out: {invalid_msgs}")
        return valid_msgs


def get_articles_generator_for(storage: InlineQueryResultsBuilder, max_description: int = 120) -> callable:
    """Generate the function that simplifies the creation of articles which text and description must be the same.
    :param storage: an instance of `InlineQueryResultsBuilder`
    :param max_description: a maximum length of the description string
    :return: a function `(title: str, text: str, **kwargs) -> None` which you should use to add new articles to the
        storage
    """
    def add_article(title: str, text: str, description: str = None, parse_mode: str = "", **kwargs) -> None:
        if not description:
            if len(text) > max_description:
                description = text[:max_description-1].rstrip() + '…'
            else:
                description = text
        storage.add(
            type='article',
            title=title,
            description=description,
            input_message_content={
                'message_text': text,
                'parse_mode': parse_mode
            },
            **kwargs
        )
    return add_article


class InlineKeyboardBuilder:
    """A builder to simplify creation of inline keyboards.

    Usage:
    >>> builder = InlineKeyboardBuilder()
    >>> row1 = builder.add_row().add("Button 1").add("Button 2")
    >>> row2 = builder.add_row().add("Button 3").add("Button 4")
    >>> keyboard = builder.build()
    """

    class RowBuilder:
        """An internal builder used to create a DSL for rows."""

        def __init__(self):
            self._cols = []

        def add(self, text: str, **kwargs) -> "InlineKeyboardBuilder.RowBuilder":
            """Append a new button to the internal list. Can be used in chains of methods.
            :param text: see https://core.telegram.org/bots/api#inlinekeyboardbutton
            """

            obj = kwargs
            obj['text'] = text
            self._cols.append(obj)
            return self

        def build(self) -> list:
            """:return: a copy of the internal list"""
            return self._cols.copy()

    def __init__(self):
        self._rows = []

    def add_row(self) -> "InlineKeyboardBuilder.RowBuilder":
        """:return: a builder object for you to fill it."""
        row_builder = InlineKeyboardBuilder.RowBuilder()
        self._rows.append(row_builder)
        return row_builder

    def build(self) -> dict:
        """:return: a dict prepared for the Bot API"""
        keyboard = [row.build() for row in self._rows.copy()]
        return {'inline_keyboard': keyboard}
