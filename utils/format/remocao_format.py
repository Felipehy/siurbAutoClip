from utils.format.format_base import FormatBase

class RemocaoFormat(FormatBase):
    
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
