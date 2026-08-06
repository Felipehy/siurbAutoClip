from dataclasses import dataclass
from datetime import datetime

@dataclass
class _Base:

    #Base que todos os outros documentos precisam ter

    orgao: str = ""
    unidade_responsavel: str = ""
    conteudo: str = ""
    id_doc: int = 0
    data_do: datetime = None


@dataclass
class Afastamento(_Base):
    nome: str = ""
    cargo: str = ""
    departamento: str = ""
    dia_inicial: datetime = None


@dataclass
class ConcessaoAposentadoria(_Base):
    nome: str = ""
    numero_processo: str = ""
    simbolo: str = ""
    cargo: str = ""
    registro_funcional: str = ""


@dataclass
class Exoneracao(_Base):
    nome: str = ""
    numero_processo: str = ""
    departamento: str = ""
    cargo: str = ""
    data: datetime = None


@dataclass
class FeriasDeferidas(_Base):
    nome: str = ""
    exercicio: str = ""
    cargo: str = ""
    quantidade_dias: int = 0
    data: datetime = None


@dataclass
class Nomeacao(_Base):
    nome: str = ""
    numero_processo: str = ""
    departamento: str = ""
    cargo: str = ""
    data: datetime = None


@dataclass
class Remocao(_Base):
    nome: str = ""
    cargo: str = ""
    departamento: str = ""
    dia_inicial: datetime = None


@dataclass
class Substituicao(_Base):
    nome: str = ""
    substituido: str = ""
    cargo_antigo: str = ""
    novo_cargo: str = ""
    cargo_sub: str = ""
    departamento: str = ""
    inicio_ferias: datetime = None
    fim_ferias: datetime = None


@dataclass
class _BaseContrato(_Base):

    #Base para os contratos de aditamento e extratos de contratos(contrados que foram assinados)

    numero_contratacao: str = ""
    numero_contrato_siurb: str = ""
    numero_processo_sei: str = ""
    tipo_objeto: str = ""
    modalidade: str = ""
    subprefeitura: str = ""
    localizacao: str = ""
    nome_credor: str = ""
    dotacao: str = ""
    cnpj_empresarial: str = ""
    descricao_objeto: str = ""
    ano_contrato: datetime = None
    prazo_contratual: datetime = None


@dataclass
class ContratosAditamento(_BaseContrato):
    pass  # herda tudo, pode adicionar campos específicos aqui


@dataclass
class ContratosExtratos(_BaseContrato):
    pass  # herda tudo, pode adicionar campos específicos aqui
