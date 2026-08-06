from utils.extract_extern.format.base_format import BaseFormat

class ImgFormat(BaseFormat):
        
    def format_contractor(self,text):

        listCheck = {
            "OBJETO",
            "CONTRATADA",
            "VALOR DO CONTRATO",
            "DOTAÇÃO A SER ONERADA",
            "NOTA DE EMPENHO",
        }

        indexContractor = text.find("CONTRATANTE:")
        if (indexContractor == -1): indexContractor = text.find("Contratante")
        
        format_text = text[indexContractor+12:]
        index2Point = format_text.find(":")
        format_text = format_text[:index2Point]

        for i in listCheck:
            if (i in format_text):
                contractor = format_text[0:((len(format_text)-1)-(len(i)-1))] 
                return contractor.replace("\n", " ").strip()
