#!/usr/bin/env python3
import json
import os
from pathlib import Path
import asyncio
from aiohttp import web
from aiotg import Bot, Chat, InlineQuery, CallbackQuery, ChosenInlineResult
from klocmod import LocalizationsContainer

from . import msgdb
from . import strconv
import usrsrvc
from .strconv.currates import update_rates_async_loop, update_volatile_rates_async_loop
from .txtproc import TextProcessorsLoader, TextProcessor, metrics
from .txtprocutil import resolve_text_processor_name, collect_help_messages, divide_chunks
from .config import *
from .config.currates_conf import EXCHANGE_RATE_SOURCES, UPDATE_VOLATILE_PERIOD_IN_HOURS
from .queryutil import *


DECRYPT_BUTTON_CACHE_TIME = 3600    # in seconds

bot = Bot(api_token=TOKEN, default_in_groups=True)
localizations = LocalizationsContainer.from_file(Path(__file__).parent / "localizations.ini")
user_service_client = usrsrvc.Client(GRPC_ADDR_USER_SERVICE)

text_processors = TextProcessorsLoader(strconv)
metrics.register(*text_processors.all_processors)

async_tasks = [
    update_rates_async_loop(EXCHANGE_RATE_SOURCES),
    update_volatile_rates_async_loop(EXCHANGE_RATE_SOURCES, UPDATE_VOLATILE_PERIOD_IN_HOURS),
]


@bot.command("/start")
@bot.command("/help")
@bot.default
async def start(chat: Chat, _) -> None:
    user = chat.message['from']
    lang_code = await user_service_client.get_lang_code(user['id'], user.get('language_code'))
    lang = localizations.get_lang(lang_code)
    messages = collect_help_messages(text_processors.all_processors, lang)
    kb = InlineKeyboardBuilder()
    for row in divide_chunks(messages, 2):
        r = kb.add_row()
        for cmd in row:
            r.add(cmd.title, callback_data=f"help:{cmd.name}")
    chat.send_text(lang['help_message'], parse_mode="Markdown", reply_markup=json.dumps(kb.build()))


@bot.callback("help:")
async def help_callback(chat: Chat, query: CallbackQuery, _: str) -> None:
    user = query.src['from']
    lang_code = await user_service_client.get_lang_code(user['id'], user.get('language_code'))
    lang = localizations.get_lang(lang_code)
    proc_name = query.data[5:]
    localized_proc_name = lang[f"hint_{proc_name}"]
    src_msg = query.src['message']
    src_text: str = src_msg.get('text')
    if src_text and localized_proc_name == src_text.partition('\n')[0]:
        query.answer(text=lang['current_help_tab'])
    else:
        messages = collect_help_messages(text_processors.all_processors, lang)
        msg = [m for m in messages if m.name == proc_name]
        answer = f"*{localized_proc_name}*\n\n{msg[0].description}"
        bot.edit_message_text(chat.id, src_msg['message_id'], answer,
                              parse_mode='Markdown',
                              reply_markup=json.dumps(src_msg['reply_markup']))


@bot.inline
async def inline_request_handler(request: InlineQuery) -> None:
    results = InlineQueryResultsBuilder()
    add_article = get_articles_generator_for(results)

    user = request.sender
    lang_code = await user_service_client.get_lang_code(user['id'], user.get('language_code'))
    lang = localizations.get_lang(lang_code)

    def transform_query(transformer: TextProcessor, **kwargs):
        processed_str = transformer.process(request.query, lang_code)
        description = transformer.get_description(request.query, lang_code)
        parse_mode = "HTML" if transformer.use_html else ""
        localized_transformer_name = resolve_text_processor_name(transformer, lang)
        add_article(localized_transformer_name, processed_str, description, parse_mode,
                    transformer.snake_case_name, **kwargs)

    exclusive_processors = text_processors.match_exclusive_processors(request.query, lang_code)
    if exclusive_processors:
        for processor in exclusive_processors:
            transform_query(processor)
    else:
        processors = text_processors.match_simple_processors(request.query, lang_code)
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
async def decrypt(_, query: CallbackQuery) -> None:
    user = query.src['from']
    lang_code = await user_service_client.get_lang_code(user['id'], user.get('language_code'))
    not_found_msg = localizations.get_phrase(lang_code, 'missing_original_text')
    message = msgdb.select(query.data) or not_found_msg
    query.answer(text=message, cache_time=DECRYPT_BUTTON_CACHE_TIME)


@bot.chosen_inline_result_callback
def chosen_inline_result_callback(chosen_result: ChosenInlineResult) -> None:
    metrics.inc(chosen_result.result_id)


async def run() -> None:
    if PROXY:
        from aiohttp_socks import ProxyConnector
        bot._connector = ProxyConnector.from_url(PROXY)

    tasks = [asyncio.create_task(t) for t in async_tasks]
    runner = None

    try:
        if DEBUG:
            await bot.delete_webhook()
            app = web.Application()
        else:
            await bot.set_webhook(f"https://{HOST}:{SERVER_PORT}/{NAME}/")
            app = bot.create_webhook_app(f"/{NAME}/")

        app.router.add_get("/metrics", metrics.handler)
        runner = web.AppRunner(app)
        await runner.setup()

        if SOCKET_TYPE == 'TCP':
            site = web.TCPSite(runner, APP_HOST, APP_PORT)
        elif SOCKET_TYPE == 'UNIX':
            os.umask(0o137)    # rw-r----- for the unix socket
            site = web.UnixSite(runner, UNIX_SOCKET)
        else:
            raise ValueError("The value of the SOCKET_TYPE environment variable is invalid!")
        await site.start()

        if DEBUG:
            await bot.loop()
        else:
            await asyncio.Event().wait()
    except asyncio.CancelledError:
        bot.stop()
    finally:
        for t in tasks:
            t.cancel()
        await bot.session.close()
        if runner is not None:
            await runner.cleanup()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        pass
