from utils.format.format_base import FormatBase

class SubstituicaoFormat(FormatBase):
    
    def format_date(self,date):
        
        listReplace = [
            "no período de",
            ".",
            "\xa0",
            "à",
            "a",
            "A",
            "á",
        ]

        formatDate = date

        for l in listReplace:
            formatDate = formatDate.replace(l,"")
            
        return formatDate.split()
