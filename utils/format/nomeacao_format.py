from utils.format.format_base import FormatBase
from utils.validate import text_size_is_bigger

class NomeacaoFormat(FormatBase):

    def format_process(self,process):
        
        format_process = process
        index = format_process.find("SEI")
        format_process = format_process[index+3:].strip().replace("\xa0", "")

        return format_process
    
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

        if (text_size_is_bigger(format_date, 10)):
            size = len(format_date) - 10
            format_date = format_date[size:]

        return format_date 