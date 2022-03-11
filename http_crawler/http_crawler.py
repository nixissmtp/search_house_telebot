from abc import abstractclassmethod
from msg_adapter import MessagesAdapter
from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen


class Crawler(MessagesAdapter):
    def __init__(self, url):
        super().__init__()
        self.url = f"{self.base_url}/{url}"

    def run(self):
        with urlopen(self.url) as doc_bytes:
            soup = Soup(doc_bytes, "html.parser")
            self.parse(soup)

    @abstractclassmethod
    def parse(self):
        pass
