from .base import Base
from sqlalchemy import Column, String


class TelegramMessage(Base):
    __tablename__ = "telegram_message"

    message = Column(String)

    def __str__(self):
        return f"{self.id}: {self.message}"
