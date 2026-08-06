from selenium.common import ElementNotVisibleException,ElementNotInteractableException,WebDriverException
from selenium.webdriver.common.by import By
from selenium import webdriver
from config.settings import SITE_URL

class MainPage():

    def __init__(self, driver: webdriver):
        self.driver = driver

    def _openGoogle(self):
        try:    
            web = self.driver

            web.get(SITE_URL)
            web.implicitly_wait(5)
        
        except WebDriverException as e:
            raise WebDriverException(e)

    def searchAnything(self):
        try:
            
            self._openGoogle()

            web = self.driver

            links = web.find_elements(by=By.CLASS_NAME, value="buscaavancadalink")
            links[0].click()
            button = web.find_element(by=By.ID, value="btnBuscaMaterias")
            button.click()
            web.implicitly_wait(10)

        except ElementNotInteractableException as e:
            raise ElementNotInteractableException(f"Erro ao buscar na pagina principal: {e}")

        except ElementNotVisibleException as e:
            raise ElementNotVisibleException(f"Erro ao buscar na pagina principal: {e}")
        
        except Exception as e:
            raise WebDriverException(f"Erro ao buscar na pagina principal: {e}")
