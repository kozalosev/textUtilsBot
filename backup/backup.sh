#!/bin/sh

DEST="remote-s3:${BACKUP_S3_BUCKET:-kozalo-backup-textutilsbot}"
TIMESTAMP=$(date +"%Y-%m-%d_%H_%M_%S")

rclone --config='/config/rclone.conf' copyto /data/messages.db "$DEST/messages_${TIMESTAMP}.db"

rclone --config='/config/rclone.conf' delete "$DEST" \
    --min-age "${BACKUP_KEEP_DAYS:-30}d" \
    --include "messages_*.db"
