#!/usr/bin/env python3

import os
import string
import asyncio
import functools
from aiohttp import web
from aiotg import Bot, Chat, InlineQuery, CallbackQuery

import msgdb
from config import *
from strconv import *
from queryutil import *
from userutil import *


ISSUES_LINK = "https://{}/issues/".format(REPO_URL)

bot = Bot(api_token=TOKEN)


@bot.command("/start")
@bot.command("/help")
async def start(chat: Chat, _) -> None:
    await chat.send_text("Привет! Я могу тебе помочь с различными преобразованием текста. Просто введи моё имя в "
                         "строке ввода сообщения через собачку, а дальше пиши любой текст. Работает в любом чате! "
                         "Но не злоупотребляй длинными сообщениями, так как я не смогу их обработать!")
    chat.send_text("Если ты хочешь предложить какое-то новое преобразование, отправь мне текст по следующему шаблону:\n"
                   "`/suggest Хочу предложить...`", parse_mode="Markdown")


@bot.command(r"/suggest\s*(.+)")
async def suggest(chat: Chat, match) -> None:
    user = chat.message['from']
    username = escape_html(get_username_or_fullname(user))

    first_line = match.group(1)
    rest_lines = chat.message['text'].split('\n')[1:]
    suggestion = escape_html(first_line + '\n' + '\n'.join(rest_lines))

    suggestion_report = "Пользователь {} <b>предлагает</b>:\n\n{}".format(username, suggestion)
    chat_with_admin = Chat(bot, OWNER_ID)
    chat_with_admin.send_text(suggestion_report, parse_mode="HTML")

    await chat.send_text("Предложение отправлено разработчику!")
    chat.send_text("Чтобы иметь возможность следить за судьбой предложения, можно дополнительно "
                   "[создать тикет на GitHub](%s)." % ISSUES_LINK,
                   parse_mode="Markdown")


@bot.command("/suggest")
def empty_suggest(chat: Chat, _) -> None:
    chat.send_text("Напиши своё предложение сразу после команды:\n`/suggest Хочу предложить...`\n\n"
                   "Либо можешь [создать новый тикет на GitHub](%s)." % ISSUES_LINK,
                   parse_mode="Markdown")


@bot.inline
def inline_request_handler(request: InlineQuery) -> None:
    results = InlineQueryResultsBuilder()
    add_article = get_articles_generator_for(results)

    if all(char in ('0', '1', ' ') for char in request.query):
        str_from_bin = bin_to_str(request.query)
        if str_from_bin:
            add_article("Притвориться человеком", str_from_bin)
    elif all(char in string.hexdigits + ' ' for char in request.query):
        str_from_hex = hex_to_str(request.query)
        if str_from_hex:
            add_article("Просто текст", str_from_hex)
    else:
        str_from_base64 = None
        if all(char in string.ascii_letters + string.digits + '+/=' for char in request.query):
            str_from_base64 = base64_to_str(request.query)

        if str_from_base64:
            add_article("Дешифровка", str_from_base64)
        elif request.query:
            msg_id = msgdb.insert(request.query)
            keyboard = InlineKeyboardBuilder()
            keyboard.add_row().add("Расшифровать", callback_data=msg_id)
            add_decryptable_article = functools.partial(add_article, reply_markup=keyboard.build())

            add_article("Проблемы с раскладкой?", switch_keyboard_layout(request.query))
            add_decryptable_article("Говорить, как робот", str_to_bin(request.query))
            add_decryptable_article("Типа программист", str_to_hex(request.query))
            add_decryptable_article("Шифровка", str_to_base64(request.query))

    request.answer(results.build_list())


@bot.callback
def decrypt(_, callback_query: CallbackQuery) -> None:
    message = msgdb.select(callback_query.data) or "Расшифровка потерялась :("
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
