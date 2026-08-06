from selenium import webdriver

class BrowserManager():

    def __init__(self):
        self.driver = webdriver.Chrome(options=self._config())
            
    def _config(self):
        option = webdriver.ChromeOptions() 
        option.add_argument("--headless=new")
        option.add_argument("--no-sandbox")
        option.add_argument("--disable-dev-shm-usage")
        option.add_argument("--disable-gpu")
        option.add_argument("--window-size=1920,1080")
        return option
    
    def quit(self):
        self.driver.quit()
        self.driver = None