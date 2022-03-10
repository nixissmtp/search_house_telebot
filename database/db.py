from sqlalchemy import create_engine, sessionmaker

engine = create_engine("sqlite:///bot.db")

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
