from abc import abstractclassmethod
from msg_adapter import MessagesAdapter
from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen


def generate_soup(url):
    with urlopen(url) as doc_bytes:
        return Soup(doc_bytes, "html.parser")


class Crawler(MessagesAdapter):
    def __init__(self, url, city):
        super().__init__()
        self.url = f"{self.base_url}/{url}"
        self.city = city

    def run(self):
        soup = generate_soup(self.url)
        self.parse(soup)

    @abstractclassmethod
    def parse(self):
        pass
