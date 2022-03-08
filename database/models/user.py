from sqlalchemy import Column, Integer, String
from .base import Base
from .base import Session


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    chat_id = Column(Integer)


def get_users():
    session = Session()
    return session.query(User).all()


def create_user(name, chat_id):
    session = Session()
    user = session.query(User).filter(User.chat_id == chat_id).scalar()
    if user:
        return False

    user = User(name=name, chat_id=chat_id)
    session.add(user)
    session.commit()
    return user


def delete_user(name):
    session = Session()
    users = session.query(User).filter(User.name == name)

    for user in users:
        session.delete(user)
        session.commit()
