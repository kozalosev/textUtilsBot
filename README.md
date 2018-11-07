[@textUtilsBot](https://t.me/textUtilsBot)
==========================================

[![Build Status](https://travis-ci.org/kozalosev/textUtilsBot.svg?branch=master)](https://travis-ci.org/kozalosev/textUtilsBot)

A simple bot for [Telegram](https://telegram.org), that has some useful handlers of inline queries to make text
conversions.

The bot supports both ways of communication with Telegram: polling (intended for debugging) and web hooks (for
production use).

**Feel free to suggest additional functionality, new features, and configuration examples!** Just create an issue or
send me a pull request.


Requirements
------------

- [Python 3.5+](https://www.python.org)
- [aiotg](https://pypi.python.org/pypi/aiotg)
- [aiohttp](https://pypi.python.org/pypi/aiohttp)

To execute the tests:

- [pytest](https://pypi.python.org/pypi/pytest)
- [coverage](https://pypi.python.org/pypi/coverage)


How to deploy
-------------

The project is supposed to be used within a virtual environment. There is a special [initialization script](init.sh),
that can help you on Linux. On Windows, you have to manually run *venv*, install all dependencies using *pip* and copy
the *config.py* file from the [`examples/`](examples) directory into [`app/`](app).

1. Clone the repository.
2. `./init.sh`
3. Configure [nginx](http://nginx.org) or any other front-end web server (keep reading for more information).
4. Edit [app/config.py](app/config.py) according to your environment.
5. Run `./start.sh` using one of the following ways:
    - directly (`nohup ./start.sh &>/dev/null &`);
    - configure [supervisord](http://supervisord.org/) or **systemd** to do it for you (see
        [exemplary configuration files](examples));
    - configure any other service manager on your choice (but you have to write configuration by yourself).

I encourage you to use the application as a local server that receives requests from Telegram from an external web
server. In such case, you can configure a TLS certificate for all at once. This is especially handy in the case if
you're using [Cloudflare](https://www.cloudflare.com/) services.

If you use *nginx*, look at [the exemplary configuration file](examples/nginx-textUtilsBot.conf). In other cases, you
have to write it by yourself (and send me a pull request, of course 😊).

Nevertheless, nobody forbids you to use the application as a front-end web server directly. However, to reach this, you
have to make some changes in [app/bot.py](app/bot.py):

```python
import ssl
...
SSL_CERT = "/your/path/to/ssl/certificate.pem"
SSL_PRIV = "/your/path/to/ssl/private.key"
...
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(SSL_CERT, SSL_PRIV)
web.run_app(app, host='0.0.0.0', port=APP_PORT, ssl_context=context)
```


How to contribute a new feature
-------------------------------

As of [v1.1.0](https://github.com/kozalosev/textUtilsBot/releases/tag/1.1.0), it became much easier to add new text
processors to the bot. If [earlier](https://github.com/kozalosev/textUtilsBot/tree/c25df0e0f246ca9c2143098d4cf7c72535b96591)
you had to embed calls of new functions into the entangled and confusing
[inline_request_handler](https://github.com/kozalosev/textUtilsBot/blob/c25df0e0f246ca9c2143098d4cf7c72535b96591/app/bot.py#L64)
function itself, now this handler is implemented by using dynamic autoloading of modules from the [strconv](app/strconv)
package. All you need is to add a new module there, implement the
[TextProcessor](https://github.com/kozalosev/textUtilsBot/blob/feb637b48fd1aa3f87c04333c08bad3fd7f38024/app/txtproc/abc.py#L12)
interface (strictly speaking in terms of Python, extend the ABC class) and append strings with a key
`hint_{classname_in_snake_case}` to the [localizations.ini](app/localizations.ini) file.

For more information, you may look at either real-world examples
([banner](https://github.com/kozalosev/textUtilsBot/blob/master/app/strconv/banner.py),
[typographer](https://github.com/kozalosev/textUtilsBot/blob/master/app/strconv/typographer.py)) or the fictional ones,
written exclusively for educational purposes, below.


### Exemplary text processor

We're gonna create a very simple and stupid text processor. Let's, for instance, search input queries for the word
`anime` and block other processors if it's found, suggesting only one message with text `Baka-chan!` ("baka" means a
fool in Japanese), stylized by the bold font.

There are several ABC and mix-in classes in the [txtproc.abc](app/txtproc/abc.py) module. The most important is the
`TextProcessor` class, of course. It defines the interface of all text processors and implements the `name` property,
used by the localization system.

Text processors can be exclusive, reversible and universal. 

The exclusivity means here that there is only a subset of processors which should handle the query. If such processors
are found, the others will be discarded. It's mostly useful for decoders.

The reversibility means, obviously, that the transformed string may be  transformed back and this reversed
transformation has sense. Mostly useful for encoders.

Universal text processors are just the processors that can handle any text. That's it.


#### Implementation

Firstly, let's look at the `TextInteface` as a whole and implement the processor without other mix-in classes.

```python
# app/strconv/baka.py

import re
# In fact, there is a shortcut for TextProcessor in the 'txtproc' module itself,
# but it's mostly intended for the loading system. Later you'll understand why
# you almost always should prefer the `abc` submodule.
from txtproc.abc import TextProcessor


class BakaDetector(TextProcessor):
    # Discard all non-exclusive processors if this one is matched.
    is_exclusive = True
    # By default, the text will be rendered by Telegram as-is.
    use_html = True
    
    # Let the system determine if the processor is able to handle a query.
    @classmethod
    def can_process(cls, query: str) -> bool:
        return re.search(r"\banime\b", query, re.IGNORECASE) is not None

    # Return the resulted message.
    def process(self, query: str) -> str:
        return "<b>Baka-chan!</b>"
    
    # Description of the message mustn't contain HTML tags since they will be rendered as-is.
    def get_description(self, query: str) -> str:
        return "Baka-chan!"
```

OK. Let's make the class a bit simpler by using the built-in mix-ins.

```python
import re
from txtproc.abc import *


# Here we describe our text processor in one line.
class BakaDetector(Exclusive, HTML, TextProcessor):    
    @classmethod
    def can_process(cls, query: str) -> bool:
        return re.search(r"\banime\b", query, re.IGNORECASE) is not None

    def process(self, query: str) -> str:
        return "<b>Baka-chan!</b>"
    
    def get_description(self, query: str) -> str:
        return "Baka-chan!"
```

Note that you're, as a text processor developer, responsible for escaping of the input query! Use the
`strconv.util.escape_html` function for that. For the same reason, you're not allowed to use Markdown, since Telegram
flavored Markdown is much harder to escape properly.

Well, let's write another simple text processor. For example, let's convert strings to sequences of their numerical
codes and vice versa.

```python
# app/strconv/char2code.py

from typing import *
from txtproc.abc import *


# The 'Encoder' class is just a shortcut for "Reversible, TextProcessor". 
class CharEncoder(Universal, Encoder):
    def process(self, query: str) -> str:
        codes = [str(ord(c)) for c in query]
        return " ".join(codes)


# The 'Decoder' class is a shortcut for "Exclusive, TextProcessor". 
class CharDecoder(Decoder):
    @classmethod
    def can_process(cls, query: str) -> bool:
        codes = query.split()
        return all(cls._try_parse_int(code) for code in codes)

    def process(self, query: str) -> str:
        codes = query.split()
        chars = [chr(int(code)) for code in codes]
        return "".join(chars)
        
    @staticmethod
    def _try_parse_int(s: str) -> Optional[int]:
        try:
            return int(s)
        except ValueError:
            return None
```

Use the `Encoder` and `Decoder` classes for pairs of reversible text processors.


#### Titles and localization

Do you know what we forgot to do? Titles for our processors, that will be used by the localization system! Let's fix it.
Go to the `localizations.ini` file and add the following lines:

```ini
# Under [DEFAULT] section
hint_baka_detector = Baka?
hint_char_encoder = Char codes
hint_char_decoder = Get the string back

...

# Under [ru] section
hint_baka_detector = Бака?
hint_char_encoder = Коды символов
hint_char_decoder = Вернуть строку обратно
```

Much better! Actually, there is one more thing we need to do. Write tests for our code!


#### Testing

> Code without tests is buggy and bad code.  
> — [Mattias Petter Johansson](https://coub.com/view/ywl7o)

Let's create files `test_baka.py` and `test_char2code.py` files inside the `tests/test_strconv/` directory.

```python
# tests/test_strconv/test_baka.py

import pytest
from strconv.baka import BakaDetector


@pytest.fixture
def processor() -> BakaDetector:
    return BakaDetector()


def test_matcher(processor):
    assert not processor.can_process("hello world")
    assert processor.can_process("hello anime")
    assert processor.can_process("Hello Anime!")


def test_processor(processor):
    assert processor.process("hello anime") == "<b>Baka-chan!</b>"
    assert processor.get_description("hello anime") == "Baka-chan!"
    
    assert processor.process("Hello Anime!") == "<b>Baka-chan!</b>"
    assert processor.get_description("Hello Anime!") == "Baka-chan!"
```

```python
# tests/test_strconv/test_baka.py

from strconv.char2code import CharEncoder, CharDecoder


def test_encoder():
    assert CharEncoder().process("hello world") == "104 101 108 108 111 32 119 111 114 108 100"


def test_decoder():
    decoder = CharDecoder()
    assert not decoder.can_process("hello world")
    assert decoder.can_process("104 101 108 108 111 32 119 111 114 108 100")
    assert decoder.process("104 101 108 108 111 32 119 111 114 108 100") == "hello world"
```

##### Run tests on Linux

```bash
PYTHONPATH=app pytest
```

##### Run tests on Windows

```cmd
set PYTHONPATH=app && pytest
```

All tests must finish successfully.


#### What's next?

At this point, our work is done, and we're ready to commit these two features and make a pull request! Surely, we won't
do it now, but if you develop a new awesome feature, feel free to send it to the upstream! All text processors have a
chance to be included in the official hosted version of the bot. Especially if they're not universal and intended for
some special cases.
