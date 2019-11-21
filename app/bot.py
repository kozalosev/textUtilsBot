#!/usr/bin/env python3

import os
import asyncio
from aiohttp import web
from aiotg import Bot, Chat, InlineQuery, CallbackQuery
from klocmod import LocalizationsContainer

import msgdb
import strconv
from txtproc import TextProcessorsLoader, TextProcessor
from data.config import *
from queryutil import *


DECRYPT_BUTTON_CACHE_TIME = 3600    # in seconds

bot = Bot(api_token=TOKEN, default_in_groups=True)
localizations = LocalizationsContainer.from_file("app/localizations.ini")
text_processors = TextProcessorsLoader(strconv)


@bot.command("/start")
@bot.command("/help")
def start(chat: Chat, _) -> None:
    lang = localizations.get_lang(chat.message['from']['language_code'])
    chat.send_text(lang['help_message'])


@bot.inline
def inline_request_handler(request: InlineQuery) -> None:
    results = InlineQueryResultsBuilder()
    add_article = get_articles_generator_for(results)
    lang = localizations.get_lang(request.sender['language_code'])

    def transform_query(transformer: TextProcessor, **kwargs):
        processed_str = transformer.process(request.query)
        description = transformer.get_description(request.query)
        parse_mode = "HTML" if transformer.use_html else ""
        localized_str_key = "hint_" + transformer.name
        add_article(lang[localized_str_key], processed_str, description, parse_mode, **kwargs)

    exclusive_processors = text_processors.match_exclusive_processors(request.query)
    if exclusive_processors:
        for processor in exclusive_processors:
            transform_query(processor)
    else:
        processors = text_processors.match_simple_processors(request.query)
        reversible_processors = [x for x in processors if x.is_reversible]
        non_reversible_processors = [x for x in processors if not x.is_reversible]

        for processor in non_reversible_processors:
            transform_query(processor)

        msg_id = msgdb.insert(request.query)
        keyboard = InlineKeyboardBuilder()
        keyboard.add_row().add(lang['decrypt'], callback_data=msg_id)
        for processor in reversible_processors:
            transform_query(processor, reply_markup=keyboard.build())

    request.answer(results.build_list())


@bot.callback
def decrypt(_, callback_query: CallbackQuery) -> None:
    not_found_msg = localizations.get_phrase(callback_query.src['from']['language_code'], 'missing_original_text')
    message = msgdb.select(callback_query.data) or not_found_msg
    callback_query.answer(text=message, cache_time=DECRYPT_BUTTON_CACHE_TIME)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    if DEBUG:
        loop.run_until_complete(bot.delete_webhook())
        bot.run(debug=True)
    else:
        webhook_future = bot.set_webhook("https://{}:{}/{}/{}".format(HOST, SERVER_PORT, NAME, TOKEN))
        loop.run_until_complete(webhook_future)
        app = bot.create_webhook_app('/{}/{}'.format(NAME, TOKEN), loop)
        os.umask(0o137)    # rw-r----- for the unix socket
        web.run_app(app, path=UNIX_SOCKET)
