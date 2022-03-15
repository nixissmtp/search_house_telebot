from database import Base, engine
from database.models import OfferCityOlx

OLX_URLS = (
    ("ivano-frankovsk/", "Франковск", True),
)


def main():
    Base.metadata.create_all(engine)
    for url_data in OLX_URLS:
        url = url_data[0]
        city = url_data[1]
        enabled = url_data[2]
        OfferCityOlx.create(url=url, city=city, enabled=enabled)


if __name__ == "__main__":
    main()
