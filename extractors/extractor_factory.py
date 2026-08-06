from extractors.documents.afastamento import AfastamentoExtractor
from extractors.documents.concessao_aposentadoria import ConcessaoAposentadoriaExtractor
# from extractors.documents.contratos import 
from extractors.documents.exoneracao import ExoneracaoExtractor
from extractors.documents.ferias_deferidas import FeriasDeferidasExtractor
from extractors.documents.nomeacao import NomeacaoExtractor
from extractors.documents.remocao import RemocaoExtractor
from extractors.documents.substituicao import SubstituicaoExtractor
from extractors.documents.contratos import ContractConsorcioExtractor,ContractComprasExtractor,ContractAditamentoExtractor

class ExtractorFactory:

    _registry = {
        1: NomeacaoExtractor,
        2: ExoneracaoExtractor,
        3: SubstituicaoExtractor,
        4: FeriasDeferidasExtractor,
        5: ConcessaoAposentadoriaExtractor,
        6: AfastamentoExtractor,
        7: RemocaoExtractor,
        8: ContractConsorcioExtractor,
        9: ContractComprasExtractor,
        10: ContractAditamentoExtractor,
    }

    @classmethod
    def create(cls, doc_type: int, driver):
        klass = cls._registry.get(doc_type)
        if not klass:
            raise ValueError(f"Tipo {doc_type} não registrado")
        return klass(driver)

