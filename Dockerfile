FROM python:3.7

WORKDIR /home/textUtilsBot

COPY requirements.txt .
RUN pip install -r requirements.txt

USER www-data
COPY app ./app

EXPOSE 8443/tcp

CMD ["python", "app/bot.py"]
