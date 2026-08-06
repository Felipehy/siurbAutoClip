from utils.format.format_base import FormatBase

class AfastamentoFormat(FormatBase):

    def format_name(self,text,repl): #4
        
        format = text

        if format.find("-") >= 1:
            indexDash = format.find("-")
            indexServer = format.find(repl)
            format = format[indexServer:indexDash]
            format = format.replace(repl, "").strip()
            return format
        
        indexServer = format.find(repl)
        format = format[indexServer:]
        format = format.replace(repl, "").strip()
        return format

    def format_date(self,text):

        listDate = []
        format = text

        if format.find(" período") != -1:
            index = format.find("período")
            format = format[index:].replace("período","").strip()
            dates = format.split("a")
            firstDate = super().format_dateExtand(dates[0])
            lastDate = super().format_dateExtand(dates[1])
            listDate.append(firstDate)
            listDate.append(lastDate)

            return listDate 
        
        elif format.find(" realizado") != -1:
            index = format.find("realizado")
            format = format[index:].replace("realizado","").replace("de","").strip()
            dates = format.split("a")
            listDate.append(dates[0].strip())
            listDate.append(dates[1].strip())

            return listDate

        elif format.find("dia") != -1:
            
            index = format.find("dia")
            format = format[index+3:].strip()
            firstDate = super().format_dateExtand(format)
            listDate.append(firstDate)
            
            return listDate 
        
        elif format.find("de") != -1:
            index = format.split("a")
            lastDate = super().format_dateExtand(index[1])
            firstDate = lastDate.replace(lastDate[:2],index[0]).replace("de","").replace(" ","").strip()

            listDate.append(firstDate)
            listDate.append(lastDate)

            return listDate
        
    def format_reason(self,text):
        
        listReason = [
            "curso",
            "Curso",
            "participar"
        ]
        listReplace = [
            "de",
            "do",
            "da",
            "\xa0",
        ]


        format = text

        for i in listReason:
            if format.find(i) >= 1:
                index = format.find(i)

                format = format[index:]
                
                for l in listReplace:
                    format = format.replace(l,"")

                return format.strip()
            