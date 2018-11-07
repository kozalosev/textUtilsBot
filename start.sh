#!/bin/sh

. bin/activate
export PYTHONPATH=app
exec app/bot.py
