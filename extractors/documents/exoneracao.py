from bs4 import BeautifulSoup
from extractors.base_extractor import BaseExtractor
from utils.extractDoc import extractExoAndNome
from datetime import date

class ExoneracaoExtractor(BaseExtractor):

    document_type = 2
    db_method = "send_exoneracao"
    today = str(date.today().strftime("%d/%m/.%y")).replace(".", "20")

    filters = {
        "Pesquisa" : "SECRETARIA MUNICIPAL DE INFRAESTRUTURA URBANA E OBRAS",
        "Orgao": "1",
        "TipoDoc": "10",
        "DataInicio": today,
    }

    def _parse(self, soup: BeautifulSoup, driver=None) -> list[dict] | None:
        all_p = soup.find_all("p")
        all_span = soup.find_all("span")
        cleanTextP = BeautifulSoup(str(all_p), "html.parser").get_text().split(",")
        cleanTextSpan = BeautifulSoup(str(all_span), "html.parser").get_text().split(",")
        all_text = BeautifulSoup(str(soup), "html.parser").get_text()

        return extractExoAndNome(cleanTextP,cleanTextSpan,all_text)

