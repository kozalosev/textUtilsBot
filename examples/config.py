TOKEN = "123456789:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Must be consistent with the path part of the location in your front-end web server configuration.
NAME = "textUtilsBot"

HOST = "bots.example.org"
APP_HOST = '0.0.0.0'                      # '0.0.0.0' for a Docker isolated network, '127.0.0.1' for a system wide nginx
APP_PORT = 8080                           # A port for a local server, which the application establishes.
SERVER_PORT = 8443                        # A port on a front-end web server.
METRICS_PORT = 8000
UNIX_SOCKET = "/tmp/textUtilsBot.sock"    # A Unix domain socket to communicate with that web server.
SOCKET_TYPE = 'TCP'                       # TCP or UNIX

# Set to 'False' for production use.
# Besides the level of verbosity, determines whether polling or webhooks will be used.
DEBUG = True
