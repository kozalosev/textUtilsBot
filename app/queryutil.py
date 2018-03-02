"""Utilities to make composing of inline query results easier."""


class InlineQueryResultsBuilder:
    """A helper class to make the creation of a result to an inline query a bit easier.
    It takes responsibility for setting proper `id`s to your `InlineQueryResult`s
    """

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
        """:return: a copy of the internal list"""
        return self._list.copy()


def get_articles_generator_for(storage: InlineQueryResultsBuilder, max_description: int = 120) -> callable:
    """Generate the function that simplifies the creation of articles which text and description must be the same.
    :param storage: an instance of `InlineQueryResultsBuilder`
    :param max_description: a maximum length of the description string
    :return: a function `(title: str, text: str) -> None` which you should use to add new articles to the storage
    """
    def add_article(title: str, text: str) -> None:
        if len(text) > max_description:
            description = text[:max_description-1].rstrip() + '…'
        else:
            description = text
        storage.add(
            type='article',
            title=title,
            description=description,
            input_message_content={
                'message_text': text
            }
        )
    return add_article
