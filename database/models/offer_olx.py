from sqlalchemy import Column, Integer, String
from .base import Base
from .base import Session


class OfferOlx(Base):
    __tablename__ = "offer_olx"
    id = Column(Integer, primary_key=True)
    offer_id = Column(String)


def get_offers():
    session = Session()
    return session.query(OfferOlx).all()


def create_offer(offer_id):
    session = Session()
    offer = session.query(OfferOlx).filter(OfferOlx.offer_id == offer_id).scalar()
    if offer:
        return False

    offer = OfferOlx(offer_id=offer_id)
    session.add(offer)
    session.commit()
    return offer


def search_offer(offer_id):
    session = Session()
    return session.query(OfferOlx).filter(OfferOlx.offer_id == offer_id).scalar()


def clear_offers():
    session = Session()
    offers = session.query(OfferOlx).all()

    for offer in offers:
        session.delete(offer)
        session.commit()
