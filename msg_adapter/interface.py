import os
from abc import ABC, abstractclassmethod
from bot import bot
from telebot.apihelper import ApiTelegramException

CHAT_ID = os.environ.get("CHAT_ID")


class MessagesAdapter(ABC):
    def __init__(self):
        self.found = []

    def send_found(self):
        for found_msg in self.found:
            try:
                bot.send_message(CHAT_ID, found_msg)
            except ApiTelegramException:
                pass

        self.found = []

    @abstractclassmethod
    def run(self):
        pass
