from .http_crawler import Crawler, generate_soup
from database.models import OfferOlx


class OlxCrawler(Crawler):

    base_url = "https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir"

    def parse_page(self, soup, offers_set):
        offers = soup.find_all("div", {"class": "offer-wrapper"})
        offers_found = []
        for offer in offers:
            data_id = offer.find_all("table")[0]["data-id"].strip()
            offers_set.add(data_id)

            if OfferOlx.find_by_offer_id(offer_id=data_id):
                continue

            OfferOlx.create(offer_id=data_id, city=self.city)

            title_cell = offer.find_all("td", {"class": "title-cell"})[0]
            link = title_cell.find_all("a")[0]

            text = link.find_all("strong")[0].text
            price = offer.find_all("p", {"class": "price"})[0].text

            bottom = offer.find_all("td", {"class", "bottom-cell"})[0]
            spans = bottom.find_all("span")
            bottom_text = ""
            for span in spans:
                bottom_text += span.text + " "

            text = text.strip()
            price = price.strip()
            bottom_text = bottom_text.strip()

            offers_found.append({
                "link": link["href"],
                "text": text,
                "price": price,
                "bottom_text": bottom_text,
            })

        return offers_found

    def parse(self, soup):
        # get all known offers by city
        offers_set = set()

        # specify paagination
        pages = 1
        bottom_navigator = soup.find("div", {"class": "pager"})
        if bottom_navigator:
            span_buttons = bottom_navigator.find_all("span", {"class": ""})
            last_button = span_buttons[-2]
            pages = int(last_button.text)

        offers = self.parse_page(soup, offers_set)

        for page in range(1, pages):
            page += 1
            url = f"{self.url}?pages={page}"
            soup = generate_soup(url)
            offers += self.parse_page(soup, offers_set)

        for i, offer in enumerate(offers):
            self.found.append(f"{offer['link']}\n{offer['text']}: {offer['price']}\n{offer['bottom_text']}")

        # # remove non orders
        all_offers = OfferOlx.get_by_city(city=self.city)
        for offer in all_offers:
            if offer.offer_id not in offers_set:
                OfferOlx.remove(id=offer.id)

        self.create_messages()
