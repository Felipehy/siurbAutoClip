from extractors.extractor_factory import ExtractorFactory
from repository.diary_repository import DiaryRepository
from core.browser_manager import BrowserManager
from pages.main_page import MainPage
from pages.search_page import SearchPage

class Orchestrator:

    def __init__(self):
        self.browser = BrowserManager()
        self.repository = DiaryRepository()
        self.searchPage = SearchPage(self.browser.driver,self.repository)
        self.mainPage = MainPage(self.browser.driver)

    def run(self, doc_types: list):

        try:            
            for doc_type in doc_types:
                try:
                    extractor = ExtractorFactory.create(doc_type,self.browser.driver)
                    links = self.search(extractor,doc_type)
                    data = self.extractDoc(extractor,doc_type,links)
                    self.repository.save(data, extractor.db_method) 
                    
                except Exception as e:
                    print(e)
                    continue
        finally:
            self.browser.quit()

    def search(self, extractor: ExtractorFactory, doc_type):

        try:
            self.mainPage.searchAnything()
            self.searchPage.setFilters(extractor.filters)
            return self.searchPage.getLinkDocs(doc_type)
        
        except Exception as e:
            raise Exception(f"tipo: {doc_type}, erro: {e}")
    
    def extractDoc(self, extractor: ExtractorFactory, doc_type: int, links: list):

        try:
            return self.searchPage.openDoc(extractor,doc_type,links)
        
        except Exception as e:
            raise Exception(f"Erro ao extrair o documento: tipo = {doc_type}, erro: {e}")
    