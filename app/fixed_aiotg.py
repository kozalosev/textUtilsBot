"""
Temporary fix a KeyError when processing the callback handler of an
inline message.

See: https://github.com/szastupov/aiotg/issues/71
"""
import re
import aiotg


class Bot(aiotg.Bot):
    def _process_callback_query(self, query):
        chat = aiotg.Chat.from_message(self, query["message"]) if "message" in query else None
        cq = aiotg.CallbackQuery(self, query)
        for patterns, handler in self._callbacks:
            match = re.search(patterns, cq.data, re.I)
            if match:
                return handler(chat, cq, match)

        # make an assumption that the inline mode is mostly used in group chats
        if chat and not chat.is_group() or self.default_in_groups:
            return self._default_callback(chat, cq)
