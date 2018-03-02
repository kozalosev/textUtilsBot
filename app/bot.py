#!/usr/bin/env python3

import logging
from aiohttp import web
from aiotg import Bot, InlineQuery

from config import *
from strconv import *
from queryutil import *


bot = Bot(api_token=TOKEN)


@bot.inline
def shrug_shoulders(request: InlineQuery) -> None:
    str_from_bin = bin_to_str(request.query)
    str_from_hex = hex_to_str(request.query)

    results = InlineQueryResultsBuilder()
    add_article = get_articles_generator_for(results)

    if str_from_bin:
        add_article("Притвориться человеком", str_from_bin)
    elif str_from_hex:
        add_article("Просто текст", str_from_hex)
    else:
        lentach_logo = "{} ¯\_(ツ)_/¯".format(request.query).lstrip()
        add_article("Пожать плечами", lentach_logo)

        if request.query:
            binary = str_to_bin(request.query)
            hex_str = str_to_hex(request.query)
            add_article("Говорить, как робот", binary)
            add_article("Типа программист", hex_str)

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
