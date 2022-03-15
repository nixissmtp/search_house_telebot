from sqlalchemy import Column, String, Boolean
from .base import Base, new_session


class OfferOlx(Base):
    __tablename__ = "offer_olx"

    offer_id = Column(String)
    city = Column(String(255))

    @new_session
    def get_by_city(cls, session, city, *args, **kwargs):
        return session.query(cls).filter(cls.city == city).all()

    @new_session
    def find_by_offer_id(cls, session, offer_id, *args, **kwargs):
        return session.query(cls).filter(cls.offer_id == offer_id).all()

    def __str__(self):
        return f"{self.id}: {self.offer_id} - {self.city}"


class OfferCityOlx(Base):
    __tablename__ = "offer_city_olx"

    url = Column(String(255))
    city = Column(String(255))
    enabled = Column(Boolean, default=False)

    @new_session
    def get_enabled(cls, session, *args, **kwargs):
        return session.query(cls).filter(cls.enabled).all()

    @new_session
    def enable(cls, session, id, *args, **kwrgs):
        offer = session.query(cls).filter(cls.id == id).scalar()
        offer.enabled = True
        session.commit()

    @new_session
    def disable(cls, session, id, *args, **kwargs):
        offer = session.query(cls).filter(cls.id == id).scalar()
        offer.enabled = False
        session.commit()

    @new_session
    def get_by_city(cls, session, city, *args, **kwrgs):
        return session.query(cls).filter(cls.city == city).scalar()
