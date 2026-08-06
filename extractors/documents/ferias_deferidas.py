from bs4 import BeautifulSoup
from extractors.base_extractor import BaseExtractor
from utils.extractDoc import extractFeriasDeferidas
from datetime import date

class FeriasDeferidasExtractor(BaseExtractor):

    document_type = 4
    db_method = "send_ferias_deferidas"
    today = str(date.today().strftime("%d/%m/.%y")).replace(".", "20")

    filters = {
        "Pesquisa" : "FÉRIAS DEFERIDAS",
        "Orgao": "12",
        "Unidade": "110002109",
        "TipoDoc": "",
        "DataInicio": today,
    }

    def _parse(self, soup: BeautifulSoup, driver=None) -> list[dict] | None:
        all_p = soup.find_all("p")
        all_span = soup.find_all("span")
        cleanTextP = BeautifulSoup(str(all_p), "html.parser").get_text().split(",")
        cleanTextSpan = BeautifulSoup(str(all_span), "html.parser").get_text().split(",")
        all_text = BeautifulSoup(str(soup), "html.parser").get_text()

        return extractFeriasDeferidas(cleanTextP,cleanTextSpan,all_text)
    
        
