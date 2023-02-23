TOKEN = "123456789:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Must be consistent with the path part of the location in your front-end web server configuration.
NAME = "textUtilsBot"

HOST = "bots.example.org"
SERVER_PORT = 8443                        # A port on a front-end web server.
METRICS_PORT = 8000
UNIX_SOCKET = "/tmp/textUtilsBot.sock"    # A Unix domain socket to communicate with that web server.

# Set to 'False' for production use.
# Besides the level of verbosity, determines whether polling or webhooks will be used.
DEBUG = True
