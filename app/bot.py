#!/usr/bin/env python3

import os
import string
import asyncio
import functools
from aiohttp import web
from aiotg import Chat, InlineQuery, CallbackQuery
from fixed_aiotg import Bot
from klocmod import LocalizationsContainer

import msgdb
from config import *
from strconv import *
from queryutil import *
from userutil import *


ISSUES_LINK = "https://{}/issues/".format(REPO_URL)

bot = Bot(api_token=TOKEN, default_in_groups=True)
localizations = LocalizationsContainer.from_file("app/localizations.ini")


@bot.command("/start")
@bot.command("/help")
async def start(chat: Chat, _) -> None:
    lang = localizations.get_lang(chat.message['from']['language_code'])
    await chat.send_text(lang['help_message'])
    chat.send_text(lang['suggest_send_suggestion'], parse_mode="Markdown")


@bot.command(r"/suggest\s*(.+)")
async def suggest(chat: Chat, match) -> None:
    user = chat.message['from']
    username = escape_html(get_username_or_fullname(user))
    lang = localizations.get_lang(user['language_code'])

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

    if all(char in ('0', '1', ' ') for char in request.query):
        str_from_bin = bin_to_str(request.query)
        if str_from_bin:
            add_article(lang['pretend_being_human'], str_from_bin)
    elif all(char in string.hexdigits + ' ' for char in request.query):
        str_from_hex = hex_to_str(request.query)
        if str_from_hex:
            add_article(lang['plain_text'], str_from_hex)
    else:
        str_from_base64 = None
        if all(char in string.ascii_letters + string.digits + '+/=' for char in request.query):
            str_from_base64 = base64_to_str(request.query)

        if str_from_base64:
            add_article(lang['unencrypted_text'], str_from_base64)
        elif request.query:
            msg_id = msgdb.insert(request.query)
            keyboard = InlineKeyboardBuilder()
            keyboard.add_row().add(lang['decrypt'], callback_data=msg_id)
            add_decryptable_article = functools.partial(add_article, reply_markup=keyboard.build())

            add_article(lang['wrong_keyboard_layout'], switch_keyboard_layout(request.query))
            add_decryptable_article(lang['speak_like_robot'], str_to_bin(request.query))
            add_decryptable_article(lang['be_like_programmer'], str_to_hex(request.query))
            add_decryptable_article(lang['encrypted_text'], str_to_base64(request.query))

    request.answer(results.build_list())


@bot.callback
def decrypt(_, callback_query: CallbackQuery) -> None:
    not_found_msg = localizations.get_phrase(callback_query.src['from']['language_code'], 'missing_original_text')
    message = msgdb.select(callback_query.data) or not_found_msg
    callback_query.answer(text=message)


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
