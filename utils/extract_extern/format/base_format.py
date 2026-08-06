import datetime
from dateutil.relativedelta import relativedelta 

class BaseFormat():
    
    def format_allText(self,text,reference):

        cleanList = [
            "\xa0",
            "\n",
            " ,",
        ]

        index = text.find(reference)
        lenRefer = len(reference)

        formatText = text[index+lenRefer:]
        
        index = formatText.find(", ")
        if index == 0: formatText = formatText[index+1:].strip()

        for i in cleanList:
            formatText = formatText.replace(i,"")
            
        return formatText

    def format_object(self,text):
        
        list = [
            "Contratante",
            "CONTRATANTE:",
            "CONTRATADA",
            "VALOR TOTAL DO CONTRATO",
            "VALOR",
            "VALOR ESTIMADO",
            "OBJETO DO ADITAMENTO",
            "DATA DE ASSINATURA",
        ]

        value = 9999 

        index = text.find("OBJETO")

        format_text = text[index+7:]

        if (format_text.find(":") != -1):
            for i in list:
                if(format_text.find(i) < value): 
                    if(format_text.find(i) != -1):
                        value = format_text.find(i)

            format_text = format_text[:value]

        return format_text.strip()

    def format_endDate(self,dateAss, qttTerm, typeTerm):
        
        format_date = dateAss.split("/")
        _qttTerm = int(qttTerm) 
        dt = datetime.datetime(int(format_date[2]),int(format_date[1]),int(format_date[0]))

        if typeTerm[0].lower() == 'm':
            format_date = dt + relativedelta(months=+_qttTerm)

        if typeTerm[0].lower() == 'a':
            format_date = dt + relativedelta(years=+_qttTerm)
            
        if typeTerm[0].lower() == 'd':
            format_date = dt + datetime.timedelta(days=+_qttTerm)
                
        return str(format_date.strftime("%d/%m/%G"))

    def format_ObjectPrice(self,text):

        index = text.find("R$")
        _text = text[index+2:]
        index = _text.find(",")
        price = _text[:index+3].strip()

        return price

    def format_ContractTerm(self,text,date):

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
            "°",
            "N",
        ]

        year = date[8:]
        nextYear = str(int(year)+1)
        lastYear = str(int(year)-1) 
        allocationNum = ""

        index = text.find("TERMO DE CONTRATO")
        _text = text[index+17:]

        if (index == -1): 
            index = text.find("N° do Contrato")
            _text = text[index+14:]
        
        if (index == -1): 
            index = text.find("TERMO DE CONTRATO NOTA TÉCNICA")
            _text = text[index+30:]

        if (index == -1): 
            index = text.find("TERMO DE ADITAMENTO")
            _text = text[index+19:]

        if (_text.find(year) <= 20 and _text.find(year) != -1):
            index = _text.find(year)
        elif (_text.find(nextYear) <= 20 and _text.find(nextYear) != -1):
            index = _text.find(nextYear)
        elif (_text.find(lastYear) <= 20 and _text.find(lastYear) != -1):
            index = _text.find(lastYear)
        else:
            for i in range(0,len(_text),1):
                if (_text[i] in listCheck): 
                    allocationNum += allocationNum.join(_text[i]) 
                else:
                    break  
            
            contractTerm = allocationNum.replace("Nº","").replace("N°","").replace("№","").strip()
            return contractTerm

        contractTerm = _text[:index+2].replace("Nº","").replace("N°","").replace("№","")
        return contractTerm.strip()

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
            
        index = _text.find("-")
        processSEI = _text[:index+2].replace("Nº","").replace("nº","").replace("N°","").replace("№","").replace(":","").strip()

        return processSEI
    
    def format_year(self,date):

        year = ""

        for i in range(len(date)-1,0,-1):

            if (i == len(date)-5): break
            
            year += year.join(date[i])

        return year[::-1]

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
        
    def format_contractor(self,text):

        listCheck = {
            "OBJETO",
            "CONTRATADA",
            "VALOR DO CONTRATO",
            "DOTAÇÃO A SER ONERADA",
            "NOTA DE EMPENHO",
        }

        indexContractor = text.find("CONTRATANTE")
        if (indexContractor == -1): indexContractor = text.find("Contratante")
        
        format_text = text[indexContractor+12:]
        index2Point = format_text.find(":")
        format_text = format_text[:index2Point]

        for i in listCheck:
            if (i in format_text):
                contractor = format_text[0:((len(format_text)-1)-(len(i)-1))] 
                return contractor.replace("\n", " ").strip()

    def format_hired(self,text):

        listCheck = {
                "OBJETO",
                "CONTRATANTE",
                "VALOR DO CONTRATO",
                "DOTAÇÃO A SER ONERADA",
                "NOTA DE EMPENHO",
            }

        indexContractor = text.find("CONTRATADA")
        format_text = text[indexContractor+12:]
        index2Point = format_text.find(":")
        format_text = format_text[:index2Point]

        for i in listCheck:
            if (i in format_text):
                contractor = format_text[0:((len(format_text)-1)-(len(i)-1))] 
                return contractor.replace("\n", " ").strip()

    def format_commitment(self,text):
        
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

        listNamesNotes = [
            "NOTA DE EMPENHO",
            "NOTA EMPENHO",
            "NOTAS DE EMPENHO",
            "NOTAS EMPENHO",
            "Nota(s) de empenho",
            "EMPENHO"
        ]

        allocationNum = ""
        indexAllocation = 0

        for i in listNamesNotes:
            if text.find(i) == -1: continue
            indexAllocation = text.find(i)

        if indexAllocation == 0: return None

        format_text = text[indexAllocation:]

        index2Point = format_text.find(":")
        format_text = format_text[index2Point+1:]
        format_text = format_text.replace("\n", "").replace("\xa0", " ")

        for i in range(0,len(format_text),1):
            if (format_text[i] in listCheck): 
                allocationNum += allocationNum.join(format_text[i]) 
            else:
                break   
        return allocationNum.strip()
        
    def doContractTerm(self, numContract: int, year: int) -> str:
        return f"{str(numContract)}/SIURB/{year}"

    def format_objects_aditamento(self,text):

        list = [
            "Contratante",
            "CONTRATANTE",
            "CONTRATADA",
            "VALOR TOTAL DO CONTRATO",
            "DATA DE ASSINATURA",
        ]

        value = 9999 

        index = text.find("OBJETO DO ADITAMENTO")

        format_text = text[index+21:]

        if (format_text.find(":") != -1):
            for i in list:
                if(format_text.find(i) < value): 
                    if(format_text.find(i) != -1):
                        value = format_text.find(i)

            format_text = format_text[:value]

        return format_text.strip()
