TOKEN = "123456789:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Must be consistent with the path part of the location in your front-end web server configuration.
NAME = "textUtilsBot"
OWNER_ID = 12345678
REPO_URL = "github.com/username/textUtilsBot"

HOST = "bots.example.org"
APP_PORT = 8080         # A port for a local server, which the application establishes.
SERVER_PORT = 8443      # A port on a front-end web server.

# Set to 'False' for production use.
# Determines whether polling or web hooks will be used.
# Also determines what will be used for logging messages: either stderr or a file.
DEBUG = True
