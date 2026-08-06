from utils.format.format_base import FormatBase

class FeriasFormat(FormatBase):
    
    def format_days(self,text):

        listReplace = [
            "Dias",
            "dias",
            "DIAS",
        ]

        day = text

        for l in listReplace:
            day = day.replace(l,"")

        return day.strip()

    def format_workout(self,text):

        listReplace = [
            "EXERCÍCIO",
            "Exercício",
            "EXERCICIO",
            "exercicio",
            "exercício",
            "\xa0",
        ]

        year = text

        for l in listReplace:

            year = year.replace(l,"")

        return year.strip()

    def format_name(self,text):
        
        name = text
        name = name.replace("\xa0", "")
        index = name.find("-")
        name = name[index+1:].strip()

        return name
