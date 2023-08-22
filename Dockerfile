FROM python:3.11-alpine

RUN apk update && \
    apk add git gcc g++ musl-dev

WORKDIR /home/textUtilsBot

COPY requirements.txt requirements-extra.txt ./
RUN pip install -r requirements.txt -r requirements-extra.txt

# www-data
USER 33
COPY app ./app

CMD ["python", "app/bot.py"]
