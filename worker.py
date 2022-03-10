from celery import Celery
from dotenv import load_dotenv
import os
from bot import bot
from threading import Thread
from http_crawler import OlxCrawler

load_dotenv()

# REDIS_HOST = "localhost"
# REDIS_PORT = "6002"

REDIS_HOST = "redis"
REDIS_PORT = "6379"

OLX_URLS = (
    "https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/ter/",
)

providers = []
for url in OLX_URLS:
    providers.append(OlxCrawler(url))


REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
REDIS_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}'
PERIOD = 60. * 1

app = Celery('Periodic parser', backend=REDIS_URL, broker=REDIS_URL)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(PERIOD, update.s(), name='Update')


@app.task
def update():
    for provider in providers:
        provider.run()


Thread(target=bot.infinity_polling).start()
