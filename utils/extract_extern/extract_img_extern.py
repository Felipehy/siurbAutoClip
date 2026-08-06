
from utils.extract_extern.format.img_format import ImgFormat

class ExtractImgExtern():

    formats = ImgFormat()

    def __init__(self,texts):
        self.texts = texts

    def extractPriceOnContract(self):
        
        for text in self.texts:
            if ("VALOR DO CONTRATO" in text or "Valor total do contrato" in text or "VALOR ESTIMADO" in text):
                price = self.formats.format_ObjectPrice(text)
                return price
                
    def extractContractTerm(self,date):

        for text in self.texts:
            if ("TERMO DE CONTRATO" in text or "N° do Contrato" in text):
                contractTerm = self.formats.format_ContractTerm(text,date)
                return contractTerm

    def extractProcessSEI(self):

        listNames = [
            "PROCESSO SEI",
            "Processo deste contrato",
            "PROCESSO ADMINISTRATIVO",
            "PROCESSO Nº",
            "Processo nº",
            "PROCESSO",
            "PROCESSO ADMINISTRATIVO Nº",
            "PROCESSO ADMNISTRATIVO N°",
        ]

        for text in self.texts:    
            for names in listNames:
                if (names in text):
                    processSei = self.formats.format_processSEI(text)
                    return processSei

    def extractAllocation(self):

        for text in self.texts:
            if ("DOTAÇÃO" in text or "Dotação" in text):
                allocationNum = self.formats.format_allocation(text)
                return allocationNum

    def extractContractor(self):

        for text in self.texts:
            if ("CONTRATANTE" in text or "Contratante" in text):
                contractor = self.formats.format_contractor(text)
                return contractor

    def extractHired(self): 
        
        for text in self.texts:
            hired = self.formats.format_hired(text)
            return hired

    def extractCommitment(self):

        for text in self.texts:    
            commitment = self.formats.format_commitment(text)
            return commitment
    
    def extractObjectAditamento(self):

        for text in self.texts:
            object_aditamento = self.formats.format_objects_aditamento(text)
            return object_aditamento
