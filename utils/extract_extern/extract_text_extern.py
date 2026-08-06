from utils.extract_extern.format.text_format import TextFormat

class ExtractTextExtern():

    formats = TextFormat()

    def __init__(self,texts):
        self.texts = texts

    def extractPriceOnContract(self):
        
        for i in range(0,len(self.texts),1):
            if ("VALOR DO CONTRATO" in self.texts[i] or "Valor total do contrato" in self.texts[i] or "VALOR ESTIMADO" in self.texts[i]):
                price = self.formats.format_ObjectPrice(self.texts[i+1])
                return price
                
    def extractContractTerm(self,date):

        for i in range(0,len(self.texts),1):
            if ("TERMO DE CONTRATO" in self.texts[i] or "N° do Contrato" in self.texts[i]):
                contractTerm = self.formats.format_ContractTerm(self.texts[i+1],date)
                return contractTerm

    def extractProcessSEI(self):

        def isProcessSEI(text) -> bool:

            for names in listNames:
                if (names in text):
                    format_text = text
                    format_text = format_text.replace(names, "").replace(".","").strip()
                if (format_text.isnumeric()):
                    return True

            return False

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

        for i in range(0,len(self.texts),1):    
            for names in listNames:
                if (names in self.texts[i]):
                    if isProcessSEI:
                        processSei = self.formats.format_processSEI(self.texts[i])
                        return processSei
                    else: 
                        processSei = self.formats.format_processSEI(self.texts[i+1])
                        return processSei
                    
    def extractAllocation(self):

        for i in range(0,len(self.texts),1):
            if ("DOTAÇÃO" in self.texts[i] or "Dotação" in self.texts[i]):
                allocationNum = self.formats.format_allocation(self.texts[i+1])
                return allocationNum

    def extractContractor(self):

        for i in range(0,len(self.texts),1):
            if ("CONTRATANTE" in self.texts[i] or "Contratante" in self.texts[i]):
                contractor = self.formats.format_contractor(self.texts[i+1])
                return contractor

    def extractHired(self): 
        
        for i in range(0,len(self.texts),1):
            if ("Contratada" in self.texts[i]):    
                hired = self.formats.format_hired(self.texts[i+1])
                return hired

    def extractCommitment(self):

        for i in range(0,len(self.texts),1):  
            if ("Nota(s) de empenho" in self.texts[i]):    
                commitment = self.formats.format_commitment(self.texts[i+1])
                return commitment

    def extractObjectAditamento(self):

        for i in range(0,len(self.texts),1):
            if ("OBJETO DO ADITAMENTO" in self.texts[i]):    
                object_aditamento = self.formats.format_objects_aditamento(self.texts[i+1])
                return object_aditamento
