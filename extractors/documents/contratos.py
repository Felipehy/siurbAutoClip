from extractors.base_extractor import BaseExtractor
from utils.extractDoc import extractContractConsorcio,extractContractCompras,extractContractAditamento
from bs4 import BeautifulSoup
from datetime import date

class ContractComprasExtractor(BaseExtractor):

    document_type = 9
    db_method = "send_contractCompras"
    today = str(date.today().strftime("%d/%m/.%y")).replace(".", "20")

    filters = {
        "Pesquisa" : "",
        "Orgao": "12",
        "Unidade": "",
        "TipoDoc": "2990",
        "DataInicio": today,
    }

    def _parse(self,soup: BeautifulSoup,driver):
        all_p = soup.find_all("p")
        all_span = soup.find_all("span")
        cleanTextP = BeautifulSoup(str(all_p), "html.parser").get_text().split(",")
        cleanTextSpan = BeautifulSoup(str(all_span), "html.parser").get_text().split(",")
        all_text = BeautifulSoup(str(all_p), "html.parser").get_text()

        return extractContractCompras(cleanTextP,cleanTextSpan,all_text,soup,driver)
    
class ContractConsorcioExtractor(BaseExtractor):

    document_type = 8
    db_method = "send_contractConsorcio"
    today = str(date.today().strftime("%d/%m/.%y")).replace(".", "20")

    filters = {
        "Pesquisa" : "",
        "Orgao": "12",
        "Unidade": "",
        "TipoDoc": "2991",
        "DataInicio": "01/01/2026"#today,
    }

    def _parse(self,soup: BeautifulSoup,driver):
        all_p = soup.find_all("p")
        all_span = soup.find_all("span")
        cleanTextP = BeautifulSoup(str(all_p), "html.parser").get_text().split(",")
        cleanTextSpan = BeautifulSoup(str(all_span), "html.parser").get_text().split(",")
        all_text = BeautifulSoup(str(all_p), "html.parser").get_text()

        return extractContractConsorcio(cleanTextP,cleanTextSpan,all_text,soup,driver)
    
class ContractAditamentoExtractor(BaseExtractor):

    
    document_type = 10
    db_method = "send_contractAditamento"
    today = str(date.today().strftime("%d/%m/.%y")).replace(".", "20")

    filters = {
        "Pesquisa" : "",
        "Orgao": "12",
        "Unidade": "",
        "TipoDoc": "2987",
        "DataInicio": "01/01/2026"#today,
    }

    def _parse(self,soup: BeautifulSoup,driver):
        all_p = soup.find_all("p")
        all_span = soup.find_all("span")
        cleanTextP = BeautifulSoup(str(all_p), "html.parser").get_text().split(",")
        cleanTextSpan = BeautifulSoup(str(all_span), "html.parser").get_text().split(",")
        all_text = BeautifulSoup(str(all_p), "html.parser").get_text()

        return extractContractAditamento(cleanTextP,cleanTextSpan,all_text,soup,driver)
    