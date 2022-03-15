from database.models import OfferCityOlx
from http_crawler import OlxCrawler


class OffersProvider:
    def run(self):
        enabled_cities = OfferCityOlx.get_enabled()
        for offer_city in enabled_cities:
            OlxCrawler(offer_city.url, offer_city.city).run()
