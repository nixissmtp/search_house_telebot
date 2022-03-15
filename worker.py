from celery import Celery
from dotenv import load_dotenv
import os
from bot import bot
from threading import Thread
from offers_provider import offers_provider
from database.models import TelegramMessage

load_dotenv()

# REDIS_HOST = "localhost"
# REDIS_PORT = "6002"

REDIS_HOST = "redis"
REDIS_PORT = "6379"
MINUTES = os.environ.get("MINUTES_PERIOD") or 1
PERIOD = 60. * int(MINUTES)
TELEGRAM_MSG_LIMITS = 10


REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
REDIS_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}'

app = Celery('Periodic parser', backend=REDIS_URL, broker=REDIS_URL)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(PERIOD, update.s(), name='Update')
    sender.add_periodic_task(30., send_messages.s(), name="Send messages to telegram")


@app.task
def update():
    offers_provider.run()


@app.task
def send_messages():
    for message in TelegramMessage.get_all(limit=TELEGRAM_MSG_LIMITS):
        if bot.send_message(message.message):
            TelegramMessage.remove(id=message.id)


Thread(target=bot.infinity_polling).start()
