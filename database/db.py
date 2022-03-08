from sqlalchemy import create_engine, sessionmaker

engine = create_engine("sqlite:///users.py")

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
