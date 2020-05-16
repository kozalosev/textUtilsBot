FROM python:3.8-alpine

RUN apk update && \
    apk add git gcc musl-dev

WORKDIR /home/textUtilsBot

COPY requirements.txt .
RUN pip install -r requirements.txt

# www-data
USER 33
COPY app ./app

CMD ["python", "app/bot.py"]
