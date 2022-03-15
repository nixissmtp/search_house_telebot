from database.models import OfferOlx

offer_models = OfferOlx.get_by_city(city="Франковск")
offers_map = {}

for offer in offer_models:
    offers_map[offer.offer_id] = offer

