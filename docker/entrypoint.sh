#!/bin/sh

if [ -n "${BACKUP_S3_BUCKET}" ] && [ -f /config/rclone.conf ]; then
    echo "${BACKUP_CRON:-0 3 * * *} /docker/backup.sh" > /var/spool/cron/crontabs/root
    crond
fi

exec su-exec 33 python app/bot.py
