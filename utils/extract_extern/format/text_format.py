from utils.extract_extern.format.base_format import BaseFormat

class TextFormat(BaseFormat):

    def format_allocation(self,text):

        listCheck = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            ".",
            "e",
            "/",
            " ",
        ]

        allocationNum = ""

        indexAllocation = text.find("DOTAÇÃO A SER ONERADA")
        if (indexAllocation == -1): indexAllocation = text.find("DOTAÇÃO SER ONERADA")
        if (indexAllocation == -1): indexAllocation = text.find("Dotação")
        if (indexAllocation == -1): indexAllocation = text.find("DOTAÇÃO")
        if (indexAllocation == -1): indexAllocation = 0
        format_text = text[indexAllocation:]

        if (format_text.find(":") <= 21):
            index2Point = format_text.find(":")
            format_text = format_text[index2Point+1:]
        else:
            format_text = format_text[7:]

        for i in range(0,len(format_text),1):
            if (format_text[i] in listCheck): 
                allocationNum += allocationNum.join(format_text[i]) 
            else:
                break   
        return allocationNum.strip()
    
    def format_processSEI(self,text):

        listProcessNames = [
            "PROCESSO SEI",
            "PROCESSO DO CONTRATO",
            "Processo deste contrato",
            "PROCESSO ADMINISTRATIVO",
            "PROCESSO ADMINISTRATIVO Nº",
            "PROCESSO ADMNISTRATIVO N°",
            "PROCESSO Nº",
            "Processo nº",
            "PROCESSO",
        ]

        for names in listProcessNames:

            index = text.find(names)
            if (index == -1): continue

            _text = text[index+len(names):]
            break
        
        if (index == -1): None

        index = _text.find("-")
        processSEI = _text[:index+2].replace("Nº","").replace("nº","").replace("N°","").replace("№","").replace(":","").strip()

        return processSEI