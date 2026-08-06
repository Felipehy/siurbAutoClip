from pdf2image import convert_from_path
from urllib.request import urlopen,Request
from bs4 import BeautifulSoup
from config.settings import POPPLER,SITE_URL,PDF_PATH#,TESSERACT
import cv2
import numpy as np
import requests
import pytesseract

class ExtractDocExtern():
    
    def extractExtern(self,html,driver):
        
        self.extractLink(html=html)
        if (self.__hasText()):
            return 1, self.extractTextFromWeb(driver)
        else:
            return 2, self.extractTextFromImages(driver)

    def __configImage(self, img):
        img_np = np.array(img)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        del img_np

        if gray.std() < 30:
            result = self.__pipelineLowContrast(gray)
        else:
            result = self.__pipelineNormal(gray)
        
        del gray

        return result

    def __pipelineNormal(self, gray):
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)[1]
        config = r'--oem 3 --psm 6'
        return config, thresh

    def __pipelineLowContrast(self, gray):
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
        thresh = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            51, 15
        )
        kernel = np.ones((2, 2), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        config = r'--oem 3 --psm 3'
        return config, thresh
    
    def __hasText(self) -> bool:
        
        req = Request(self.__link)
        response = urlopen(req)
        html = response.read()
        
        try:
            soup = BeautifulSoup(html,"html.parser")
        except:
            return False
        
        all_p = soup.find_all('p')

        texts = [p.get_text(strip=True) for p in all_p if p.get_text(strip=True)]

        for t in texts:
            if ("startxref" in t or "%%EOF" in t or "�" in t): return False

        if (not texts):
            return False
        
        return True

    def extractLink(self,html):
        self.__linkData = html.find('a')
        self.__link = self.__linkData.get("href")  

    def extractTextFromWeb(self,driver):

        original_tab = driver.current_window_handle

        driver.switch_to.new_window('tab')
        driver.get(self.__link)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        all_p = soup.find_all('p')
        
        cleanTextP = BeautifulSoup(str(all_p), "html.parser").get_text().split(',')

        driver.close()
        driver.switch_to.window(original_tab)
        
        return cleanTextP

    def extractTextFromImages(self,driver):
        
        texts = []

        #ambiente de desenvolvimento
        # pytesseract.pytesseract.tesseract_cmd = TESSERACT

        session_cookies = {c['name']: c['value'] for c in driver.get_cookies()}

        response = requests.get(self.__link, cookies=session_cookies)

        with open(PDF_PATH, "wb") as f:
            f.write(response.content)
        
        images = convert_from_path(
            PDF_PATH,
            poppler_path=POPPLER,
            dpi=400,
            first_page=1,
            last_page=2,
        )

        for i,img in enumerate(images):

            config, thresh = self.__configImage(img)
            texts.append(pytesseract.pytesseract.image_to_string(thresh, lang="por", config=config))
            del thresh

        return texts