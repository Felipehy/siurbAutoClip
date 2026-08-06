from bs4 import BeautifulSoup
from abc import abstractmethod,ABC
from selenium.webdriver.remote.webdriver import WebDriver
from urllib.request import Request,urlopen

class BaseExtractor(ABC):

    def __init__(self,driver):
        self.driver = driver

    def extract(self, url:str) -> list[dict] | None:

        soup = self._fetch_soup(url)
        if soup is None:
            return None
        return self._parse(soup,self.driver)

    def _fetch_soup(self, url:str) -> BeautifulSoup | None:
        
        try:
            req = Request(url)
            html = urlopen(req).read()
            return BeautifulSoup(html, "html.parser")
        except Exception as e:
            print(f"Erro ao buscar {url}: {e}")
            return None
    
    @abstractmethod
    def _parse(self,soup: BeautifulSoup, driver: WebDriver | None = None) -> list[dict] | None:
        ...

    @property
    @abstractmethod
    def document_type(self) -> int:
        ...
    
    @property
    @abstractmethod
    def db_method(self) -> str:
        ...
    
