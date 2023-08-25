FROM python:3.11-alpine as builder

RUN apk update && \
    apk add --no-cache git gcc g++ musl-dev

COPY requirements-extra.txt ./
RUN pip wheel --wheel-dir=/root/wheels -r requirements-extra.txt


FROM python:3.11-alpine
WORKDIR /home/textUtilsBot

COPY requirements.txt requirements-extra.txt ./
COPY --from=builder /root/wheels ./wheels

RUN apk update && \
    apk add --no-cache git libstdc++

RUN pip install -r requirements.txt
RUN pip install --no-index --find-links=./wheels -r requirements-extra.txt \
    && rm -r ./wheels

# www-data
USER 33
COPY app ./app

CMD ["python", "app/bot.py"]
