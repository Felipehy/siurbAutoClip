import datetime
from dateutil.relativedelta import relativedelta 

class FormatBase:

    def format_name(self,text):
        
        listReplace = [
            "\xa0",
            "\'",
            "Exoneraro senhor",
            "Exonerar o senhor",
            "Exonerar a senhora ",
            "Nomear o senhor ",
            "Nomear a senhora ",
            "Nomear o senhor",
            "Nomear a senhora",
            "em substituição a",
            " Interessados:",
            " Interessado:",
            " Interessadas:",
            " Interessada:",
            " INTERESSADO:",
            " INTERESSADA:",
        ]

        name = text
        if name.find("-") > 1:
            index = name.find("-")
            name = name[:index-1]
        for i in listReplace:
            name = name.replace(i,"")
        name = name.strip()

        return name

    def format_position(self,pos):

        format_position = pos
        format_position = format_position.replace("\xa0", " ")
        index = format_position.find("de")
        format_position = format_position[index+2:].strip()

        return format_position

    def format_dateExtand(self,date):
        
        dict = {
            "01": "janeiro",
            "02": "fevereiro",
            "03": "março",
            "04": "abril",
            "05": "maio",
            "06": "junho",
            "07": "julho",
            "08": "agosto",
            "09": "setembro",
            "10": "outubro",
            "11": "novembro",
            "12": "dezembro"
        }

        format_date = date
        format_date = format_date.replace("\xa0", "").strip()

        index = format_date.find("de")
        if format_date.find("Portaria") == 0: format_date = format_date[index:]

        index = format_date.find("de")
        if index == 0: format_date = format_date[index+2:]

        format_date = format_date.replace(" de ","/")
        if format_date.find("de") != 0: format_date = format_date.replace(" de","/")

        format_date = format_date.replace(" ", "")
        format_date = format_date.replace(".", "")
        

        for key in dict:
            if dict[key] in format_date:
                format_date = format_date.replace(f"{dict[key]}", f"{key}")

        return format_date    

    def format_date(self,date):
        
        if "partir" in date:
            
            if (date.find("de") == 0):

                index = date.find("de")
                format_date = date[index+2].strip()

                return format_date

        format_date = date.split()
        format_date = format_date[len(format_date)-1]
        format_date = format_date.replace(".","")

        return format_date

    def format_department(self,depart):

        if "Gabinete" in depart:
            
            if (depart.find("do") == 0):
                format_depart = depart.strip()
                format_depart = depart[2:]
                format_depart = format_depart.replace("\xa0", "").strip()
                return format_depart
            
            return depart.replace("do", "").replace("\xa0","").strip()
        
        if "Assessoria" in depart:
            format_depart = depart.replace("da","").replace("\xa0","").strip()
            format_depart = depart.replace("para a ", "").strip()
            return format_depart

        format_depart = depart
        index = format_depart.find("de")
        format_depart = format_depart[index+2:].replace("\xa0","").strip()

        return format_depart

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
