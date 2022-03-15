from abc import ABC, abstractclassmethod
from database.models import TelegramMessage


class MessagesAdapter(ABC):
    def __init__(self):
        self.found = []

    def create_messages(self):
        for i, found_msg in enumerate(self.found):
            msg = f"{i} {self.city}: {found_msg}\n{'-' * 20}\n"
            TelegramMessage.create(message=msg)

        self.found = []

    @abstractclassmethod
    def run(self):
        pass
