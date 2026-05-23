from os import getenv as env

TOKEN = env("TOKEN")
HOST = env("HOST")  # required when DEBUG=false (webhook mode)

# Must be consistent with the path part of the location in your front-end web server configuration.
NAME = env("BOT_NAME", "textUtilsBot")

APP_HOST = env("APP_HOST", "0.0.0.0")                      # '0.0.0.0' for a Docker isolated network, '127.0.0.1' for a system wide nginx
APP_PORT = int(env("APP_PORT", "8080"))                    # A port for a local server, which the application establishes.
SERVER_PORT = int(env("SERVER_PORT", "443"))               # A port on a front-end web server.
UNIX_SOCKET = env("UNIX_SOCKET", f"/tmp/${NAME}.sock")     # A Unix domain socket to communicate with that web server.
SOCKET_TYPE = env("SOCKET_TYPE", "TCP")                    # TCP or UNIX

GRPC_ADDR_USER_SERVICE = env("GRPC_ADDR_USER_SERVICE")
USER_SERVICE_CACHE_MAX_SIZE = int(env("USER_SERVICE_CACHE_MAX_SIZE", "128"))
USER_SERVICE_CACHE_TIME = int(env("USER_SERVICE_CACHE_TIME", "300"))

# Use a proxy server to reach Telegram servers if you live in an authoritarian country
PROXY = env("PROXY")

# Set to 'False' for production use.
# Besides the level of verbosity, determines whether polling or webhooks will be used.
DEBUG = env("DEBUG", "true").lower() in ("true", "1", "yes")
