from abc import ABC, abstractclassmethod
from bot import bot
from telebot.apihelper import ApiTelegramException
from database.models import get_users


class MessagesAdapter(ABC):
    def __init__(self):
        self.found = []

    def send_found(self):
        users = get_users()
        for user in users:
            for found_msg in self.found:
                try:
                    bot.send_message(user.chat_id, found_msg)
                except ApiTelegramException:
                    pass

        self.found = []

    @abstractclassmethod
    def run(self):
        pass
