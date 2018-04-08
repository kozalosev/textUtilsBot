TOKEN = "123456789:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Must be consistent with the path part of the location in your front-end web server configuration.
NAME = "textUtilsBot"
OWNER_ID = 12345678
REPO_URL = "github.com/username/textUtilsBot"

HOST = "bots.example.org"
SERVER_PORT = 8443                        # A port on a front-end web server.
UNIX_SOCKET = "/tmp/textUtilsBot.sock"    # A Unix domain socket to communicate with that web server.

# Set to 'False' for production use.
# Besides the level of verbosity, determines whether polling or webhooks will be used.
DEBUG = True
