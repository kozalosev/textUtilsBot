#!/usr/bin/env python3

import string
import logging
from aiohttp import web
from aiotg import Bot, Chat, InlineQuery

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
                         "строке ввода сообщения через собачку, а дальше пиши любой текст. Работает в любом чате!")
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

    if all(map(lambda char: char in (0, 1), request.query)):
        str_from_bin = bin_to_str(request.query)
        if str_from_bin:
            add_article("Притвориться человеком", str_from_bin)
    elif all(map(lambda char: char in string.hexdigits, request.query)):
        str_from_hex = hex_to_str(request.query)
        if str_from_hex:
            add_article("Просто текст", str_from_hex)
    elif all(map(lambda char: char in string.ascii_letters + string.digits + '+/=', request.query)):
        str_from_base64 = base64_to_str(request.query)
        if str_from_base64:
            add_article("Дешифровка", str_from_base64)
    elif request.query:
        add_article("Проблемы с раскладкой?", switch_keyboard_layout(request.query))
        add_article("Говорить, как робот", str_to_bin(request.query))
        add_article("Типа программист", str_to_hex(request.query))
        add_article("Шифровка", str_to_base64(request.query))

    request.answer(results.build_list())


if __name__ == '__main__':
    bot.delete_webhook()
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
        bot.run()
    else:
        logging.basicConfig(filename='log.txt', filemode='w')
        bot.set_webhook("https://{}:{}/{}/{}".format(HOST, SERVER_PORT, NAME, TOKEN))
        app = bot.create_webhook_app('/{}/{}'.format(NAME, TOKEN))
        web.run_app(app, host='127.0.0.1', port=APP_PORT)
