from utils.extract_extern.extract_img_extern import ExtractImgExtern
from utils.extract_extern.extract_text_extern import ExtractTextExtern
from utils.extract_doc_extern import ExtractDocExtern
from utils.extract_extern.format.img_format import ImgFormat
from utils.extract_extern.format.text_format import TextFormat 

class ExtractExternFactory():

    _registry = {
        1: ExtractTextExtern,
        2: ExtractImgExtern,
    }

    @classmethod
    def create(cls,html,driver):

        extract = ExtractDocExtern()
        type, texts = extract.extractExtern(html=html, driver=driver)

        klass = cls._registry.get(type)

        if type == 1:
            formats = TextFormat()
        elif type == 2:
            formats = ImgFormat()
        
        if not klass:
            raise ValueError(f"O {type} não foi registrado")

        return formats ,klass(texts)
