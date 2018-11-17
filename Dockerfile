FROM python:3.7-alpine

RUN apk update && \
    apk add git

WORKDIR /home/textUtilsBot

COPY requirements.txt .
RUN pip install -r requirements.txt

# www-data
USER 33
COPY app ./app

EXPOSE 8443/tcp

CMD ["python", "app/bot.py"]
