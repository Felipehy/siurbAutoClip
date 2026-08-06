from selenium.common import ElementNotVisibleException,ElementNotInteractableException,WebDriverException
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium import webdriver
from json import dumps
from repository.diary_repository import DiaryRepository
from extractors.extractor_factory import ExtractorFactory
from time import sleep
from datetime import date

class SearchPage():

    def __init__(self, driver: webdriver, repository: DiaryRepository):
        self.driver = driver
        self.repository = repository
        self.today = str(date.today().strftime("%d/%m/.%y")).replace(".", "20")

    def setFilters(self,filters: dict):
        
        try:

            web = self.driver
        
            if filters.get("Pesquisa") != None and filters["Pesquisa"] != "":    
                sleep(2)    
                inputSearch = web.find_element(by=By.ID, value="textTermoPesquisa")
                inputSearch.clear()
                sleep(2)
                inputSearch.send_keys(filters["Pesquisa"])
                sleep(1)
            web.implicitly_wait(10)

            if filters.get("Orgao") != None and filters["Orgao"] != "":
                selectOrgan = web.find_element(by=By.ID, value="orgaosBootstrapSelect")
                selectOptionO = Select(selectOrgan)
                sleep(0.1)
                selectOptionO.select_by_value(filters["Orgao"])
            web.implicitly_wait(10)

            if filters.get("Unidade") != None  and filters["Unidade"] != "":
                selectUnit = web.find_element(by=By.ID,value="unidadeResponsavelFiltro")
                selectOptionU = Select(selectUnit)
                sleep(0.1)
                selectOptionU.select_by_value(filters["Unidade"])
            web.implicitly_wait(10)

            if filters.get("TipoDoc") != None and filters["TipoDoc"] != "":
                selectTypeDoc = web.find_element(by=By.ID, value="selectTipoDocumento")
                selectOptionT = Select(selectTypeDoc)
                sleep(0.1)
                selectOptionT.select_by_value(filters["TipoDoc"])
            web.implicitly_wait(10)

            if filters.get("DataInicio") != None and filters["DataInicio"] != "":
                #Clica no botão personalizar
                inputData = web.find_element(by=By.ID, value="abrePesquisaPeriodo")
                inputData.click()
                sleep(0.8)
                #Coloca a data de inicio
                inputText = web.find_element(by=By.ID, value="dateInicio")
                inputText.clear()
                sleep(2)
                inputText.send_keys(filters["DataInicio"])

                #Coloca a data de hoje
                inputDataFinal = web.find_element(by=By.ID, value="dateFim")
                inputDataFinal.clear()
                sleep(2)
                inputDataFinal.send_keys(self.today)

            btnFilter = web.find_element(by=By.ID, value="btnFiltrar")
            btnFilter.click() 
            sleep(2)
        
        except ElementNotInteractableException as e:
            raise ElementNotInteractableException(f"Erro ao aplicar os filtros: {e}")

        except ElementNotVisibleException as e:
            raise ElementNotVisibleException(f"Erro ao aplicar os filtros: {e}")
        
        except Exception as e:
            raise WebDriverException(f"Erro ao aplicar os filtros: {e}")

    def getLinkDocs(self, doc_type: int):
        
        try:

            _listLink = []
            _listIdDoc = []


            web = self.driver
            db = self.repository
            finish = False
    
            while not finish:
                
                links = web.find_elements(by=By.CLASS_NAME, value="nroSei")
                linkPages = web.find_elements(by=By.CLASS_NAME, value="page-link")

                for link in links:
                    if link.text.isnumeric():
                        sleep(0.25)
                        hasDocOnDB = db.has_doc(link.text,doc_type)
                        
                        if not hasDocOnDB and link.text not in _listIdDoc:
                            url = link.get_attribute("href")
                            _listLink.append(url)

                        _listIdDoc.append(link.text)

                if linkPages == []: finish = True

                for linkPage in linkPages:

                    if linkPage.text == "Próximo":
                        linkPage.click()
                        sleep(2)
                        break
        
                    if linkPage.text == linkPages[len(linkPages)-1].text:
                        finish = True 

            return _listLink
        
        except ElementNotVisibleException as e:
            raise ElementNotVisibleException(f"Não foi possivel interagir com pagina: {e}")
        
        except Exception as e:
            raise WebDriverException(f"Erro inesperado: {e}")
        
    def openDoc(self, extractor: ExtractorFactory, doc_type: int, listLinks: list):

        listExtracted = []

        for url in listLinks:
            try:
                sleep(0.25)
                data = extractor.extract(url)
                if data is None: continue

                listExtracted.append(data)

            except Exception as e:
                print(f"Error unexpected: {e}")
                continue

        return listExtracted
