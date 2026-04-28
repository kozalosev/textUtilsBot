#!/bin/sh

if [ -f .env ]; then
    set -a
    . ./.env
    set +a
fi
. venv/bin/activate
exec python -m app.bot
