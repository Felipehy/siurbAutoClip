from utils.format.format_base import FormatBase

class ConcessaoFormat(FormatBase):
    
    def format_symbol(self,text):

        fs = text

        fs = fs.replace("Símbolo:", "").strip()

        return fs

    def format_regFunc(self,text):

        fr = text

        fr = fr.replace("Registro Funcional:","").strip()

        return fr

    def format_numProc(self,text):

        format_num = text

        index = format_num.find("-")
        format_num = format_num[:index-1]
        format_num = format_num.replace("\xa0", "").strip()

        return format_num

    def format_position(self,pos):
        
        fp = pos

        fp = fp.replace("Cargo:","").strip()

        return fp

