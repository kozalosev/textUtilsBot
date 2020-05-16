#!/usr/bin/env python3

import os
import asyncio
import logging
from aiohttp import web
from aiotg import Bot, Chat, InlineQuery, CallbackQuery
from klocmod import LocalizationsContainer
from typing import *

import msgdb
import strconv
from strconv.util import escape_html
from txtproc import TextProcessorsLoader, TextProcessor
from data.config import *
from queryutil import *
from userutil import *
from timeoututil import *


ISSUES_LINK = "https://{}/issues/".format(REPO_URL)
DECRYPT_BUTTON_CACHE_TIME = 3600    # in seconds
MAX_SUGGESTIONS = 5
MAX_SUGGESTIONS_TIMEOUT = 720       # in minutes

bot = Bot(api_token=TOKEN, default_in_groups=True)
localizations = LocalizationsContainer.from_file("app/localizations.ini")
text_processors = TextProcessorsLoader(strconv)
logger = logging.getLogger(__name__)

UserId = str
suggestion_counters = {}    # type: Dict[UserId, SuggestionsCounter]


@bot.command("/start")
@bot.command("/help")
@bot.default
async def start(chat: Chat, _) -> None:
    lang = localizations.get_lang(chat.message['from']['language_code'])
    await chat.send_text(lang['help_message'])
    await chat.send_text(lang['help_message_transformers_list'])
    processors_except_decoders = [x for x in text_processors.all_processors if not x.name.endswith("decoder")]
    for processor in processors_except_decoders:
        processor_name_key, help_message_key = 'hint_' + processor.name, 'help_' + processor.name
        localized_processor_name, localized_help_message = lang[processor_name_key], lang[help_message_key]
        # skip empty and undefined help messages
        if len(localized_help_message.strip()) == 0 or localized_help_message == help_message_key:
            continue
        answer = f"*{localized_processor_name}*\n\n{localized_help_message}"
        await chat.send_text(answer, parse_mode="Markdown")
    chat.send_text(lang['suggest_send_suggestion'], parse_mode="Markdown")


@bot.command(r"/suggest\s*(.+)")
async def suggest(chat: Chat, match) -> None:
    user = chat.message['from']
    username = escape_html(get_username_or_fullname(user))
    lang = localizations.get_lang(user['language_code'])

    if user['id'] not in suggestion_counters:
        suggestion_counters[user['id']] = SuggestionsCounter()
    counter = suggestion_counters[user['id']]
    counter.increment()
    timeout_in_minutes = compute_timeout_in_minutes(counter, MAX_SUGGESTIONS, MAX_SUGGESTIONS_TIMEOUT)
    logger.debug(counter)
    logger.debug("User ID: %d, username: %s, timeout: %d minutes", user['id'], username, timeout_in_minutes)
    if counter.minutes_elapsed >= timeout_in_minutes:
        counter.reset()
    counter.update_timestamp()
    if counter.value > MAX_SUGGESTIONS:
        chat.send_text(lang['suggestion_timeout'].format(timeout_in_minutes))
        return

    first_line = match.group(1)
    rest_lines = chat.message['text'].split('\n')[1:]
    suggestion = escape_html(first_line + '\n' + '\n'.join(rest_lines))

    suggestion_report = lang['suggestion_report_template'].format(username, suggestion)
    chat_with_admin = Chat(bot, OWNER_ID)
    chat_with_admin.send_text(suggestion_report, parse_mode="HTML")

    await chat.send_text(lang['suggestion_sent'])
    chat.send_text(lang['suggest_create_issue'].format(ISSUES_LINK), parse_mode="Markdown")


@bot.command("/suggest")
def empty_suggest(chat: Chat, _) -> None:
    how_suggest_feature = localizations.get_phrase(chat.message['from']['language_code'], 'how_suggest_feature')
    chat.send_text(how_suggest_feature.format(ISSUES_LINK), parse_mode="Markdown")


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
