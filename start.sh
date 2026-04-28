#!/bin/sh

[ -f .env ] && . .env
. venv/bin/activate
exec python -m app.bot
