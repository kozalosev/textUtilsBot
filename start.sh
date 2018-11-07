#!/bin/sh

. venv/bin/activate
export PYTHONPATH=app
exec app/bot.py
