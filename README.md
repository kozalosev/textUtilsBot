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
