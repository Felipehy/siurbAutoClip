from utils.format.format_base import FormatBase

class ExoneracaoFormat(FormatBase):
    
    def format_process(self,process):
        
        format_process = process
        index = format_process.find("SEI")
        format_process = format_process[index+3:].strip().replace("\xa0", "")

        return format_process
