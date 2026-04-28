FROM python:3.14-alpine AS builder

RUN apk update && \
    apk add --no-cache git gcc g++ musl-dev

COPY requirements-extra.txt ./
RUN pip wheel --wheel-dir=/root/wheels -r requirements-extra.txt


FROM python:3.14-alpine
WORKDIR /home/textUtilsBot

COPY requirements.txt requirements-extra.txt requirements-proxy.txt ./
COPY --from=builder /root/wheels ./wheels

RUN apk update && \
    apk add --no-cache git libstdc++ rclone su-exec

RUN pip install -r requirements.txt -r requirements-proxy.txt
RUN pip install --no-index --find-links=./wheels -r requirements-extra.txt \
    && rm -r ./wheels

COPY docker/backup.sh /docker/backup.sh
COPY docker/entrypoint.sh /docker/entrypoint.sh
RUN chmod +x /docker/backup.sh /docker/entrypoint.sh

COPY app ./app

ENTRYPOINT ["/docker/entrypoint.sh"]
