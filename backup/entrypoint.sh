#!/bin/sh

if [ ! -f /config/rclone.conf ]
then
    echo "Mount your rclone.conf file to /config/rclone.conf"
    exit 1
fi

echo "${BACKUP_CRON:-0 3 * * *} /backup.sh >> /var/log/backup.log 2>&1" | crontab -

crond -f -l 2
