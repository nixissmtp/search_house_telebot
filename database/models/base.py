from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker


DB_ENGINE_CONFIG = {
    "url": "sqlite:///bot.db",
    "connect_args": {"check_same_thread": False}
}

engine = create_engine(**DB_ENGINE_CONFIG)
Session = sessionmaker(bind=engine)


def new_session(attr_method):
    @classmethod
    def wrapper(*args, **kwargs):
        session = Session()
        return attr_method(session=session, *args, **kwargs)

    return wrapper


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)

    @new_session
    def get_all(cls, session, limit=None):
        queryset = session.query(cls)
        if limit:
            queryset = queryset.limit(limit)
        return queryset.all()

    @new_session
    def create(cls, session, *args, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
        return obj

    @new_session
    def remove(cls, session, id, *args, **kwargs):
        obj = session.query(cls).filter(cls.id == id).scalar()

        if obj:
            session.delete(obj)
            session.commit()

    @new_session
    def find(cls, session, id, *args, **kwargs):
        return session.query(cls).filter(cls.id == id).scalar()

    def __str__(self):
        return str(self.id)


Base = declarative_base(cls=Base)
