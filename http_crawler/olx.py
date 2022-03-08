from .http_crawler import Crawler
from database.models import search_offer, create_offer


class OlxCrawler(Crawler):
    def parse(self, soup):
        offers = soup.find_all("div", {"class": "offer-wrapper"})
        for offer in offers:
            data_id = offer.find_all("table")[0]["data-id"]

            if search_offer(data_id):
                continue

            create_offer(data_id)

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

            msg = f"{link['href']}\n{text}: {price}\n{bottom_text}"
            self.found.append(msg)

        self.send_found()
