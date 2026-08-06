# SiurbAutoClip

> Repositório: https://github.com/Felipehy/siurbAutoClip

Robô de automação (RPA) que coleta, extrai e armazena publicações do **Diário Oficial**
relacionadas à **Secretaria Municipal de Infraestrutura Urbana e Obras (SIURB)**.

A aplicação navega pelo site do diário com Selenium, localiza as matérias de interesse,
extrai o conteúdo (por HTML ou por **OCR**, quando o documento é uma imagem/PDF),
estrutura os dados e os persiste em um banco **MySQL** — evitando duplicidades.

---

## Índice

- [Tipos de documento suportados](#tipos-de-documento-suportados)
- [Como funciona](#como-funciona)
- [Arquitetura](#arquitetura)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração (variáveis de ambiente)](#configuração-variáveis-de-ambiente)
- [Execução](#execução)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Segurança](#segurança)

---

## Tipos de documento suportados

Cada tipo é identificado por um número (usado no *factory* e no *registry* do repositório):

| ID | Documento               |
|----|-------------------------|
| 1  | Nomeação                |
| 2  | Exoneração              |
| 3  | Substituição            |
| 4  | Férias deferidas        |
| 5  | Concessão de aposentadoria |
| 6  | Afastamento             |
| 7  | Remoção                 |
| 8  | Contrato — consórcio    |
| 9  | Contrato — compras      |
| 10 | Contrato — aditamento   |

## Como funciona

1. **Busca** — abre o site do diário, aplica os filtros de cada tipo de documento
   (órgão, unidade, tipo, período) e coleta os links das matérias, paginando até o fim.
2. **Deduplicação** — antes de extrair, consulta o banco (`has_doc`) para pular
   documentos já processados.
3. **Extração** — lê o conteúdo da matéria. Quando o texto está disponível em HTML,
   usa BeautifulSoup; quando é imagem/PDF, baixa o arquivo e aplica **OCR**
   (OpenCV para pré-processamento + Tesseract).
4. **Estruturação** — normaliza os campos em objetos por tipo de documento
   (ver `models/document.py`).
5. **Persistência** — grava os registros nas tabelas correspondentes do MySQL.

O `main.py` distribui os 10 tipos de documento entre **3 workers** paralelos
(`multiprocessing.Pool`).

## Arquitetura

```
main.py            → ponto de entrada; paraleliza os tipos de documento
orchestrator.py    → coordena busca, extração e persistência de cada tipo
core/              → gerenciamento do navegador (Selenium/Chrome headless)
pages/             → Page Objects (busca e aplicação de filtros)
extractors/        → factory + extratores por tipo de documento
utils/             → parsing, formatação e OCR
repository/        → persistência no MySQL
models/            → dataclasses que representam cada documento
config/            → carregamento de configuração via variáveis de ambiente
```

## Pré-requisitos

- **Python 3.11**
- **Google Chrome** + **ChromeDriver** compatível (usado em modo headless)
- **Poppler** — conversão de PDF em imagem (`pdf2image`)
- **Tesseract OCR** com o pacote de idioma **português** (`por`)
- **MySQL** acessível com um banco `db_diario` e as tabelas dos documentos

> No Windows, o Poppler já está incluído na pasta `poppler-25.12.0/`.
> O caminho do Tesseract pode ser informado via variável de ambiente (ver abaixo).

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/Felipehy/siurbAutoClip.git
cd siurbAutoClip

# 2. Crie e ative um ambiente virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt
```

## Configuração (variáveis de ambiente)

Nenhum segredo fica versionado. Copie o arquivo de exemplo e preencha os valores:

```bash
cp .env.example .env
```

Variáveis disponíveis:

| Variável        | Obrigatória | Descrição                                                        |
|-----------------|-------------|------------------------------------------------------------------|
| `HOST_DB`       | Sim         | Host do MySQL                                                    |
| `USER_DB`       | Sim         | Usuário do MySQL                                                 |
| `PASSWD_DB`     | Sim         | Senha do MySQL                                                   |
| `SITE_URL`      | Sim         | URL do Diário Oficial a ser consultado                          |
| `PATH_ENV`      | Não         | Caminho alternativo do `.env` (default: `.env` na raiz)         |
| `PDF_PATH`      | Não         | Arquivo temporário para o PDF baixado no OCR                     |
| `POPPLER_PATH`  | Não         | Diretório dos binários do Poppler                               |
| `TESSERACT_CMD` | Não         | Caminho do `tesseract.exe` (Windows). No Linux, deixe vazio.    |

## Execução

Com o ambiente ativado e o `.env` configurado:

```bash
python main.py
```

## Estrutura do projeto

```
SiurbAutoClip/
├── main.py                 # Ponto de entrada (paralelização)
├── orchestrator.py         # Orquestração do fluxo
├── config/
│   └── settings.py         # Configuração via variáveis de ambiente
├── core/
│   └── browser_manager.py  # Selenium / Chrome headless
├── pages/                  # Page Objects (busca e filtros)
├── extractors/             # Factory + extratores por tipo
│   └── documents/
├── utils/                  # Parsing, formatação e OCR
├── repository/
│   └── diary_repository.py # Persistência no MySQL
├── models/
│   └── document.py         # Dataclasses dos documentos
├── pdfs/                   # PDFs temporários (não versionados)
├── poppler-25.12.0/        # Binários do Poppler (Windows)
├── .env.example            # Modelo de configuração
└── requirements.txt
```

## Segurança

- **Segredos** (credenciais de banco, URL) são lidos **apenas de variáveis de ambiente**.
  O arquivo `.env` está no `.gitignore` e **nunca** deve ser versionado.
- **PDFs baixados** em runtime ficam em `pdfs/` e são ignorados pelo Git
  (`pdfs/*.pdf`), pois podem conter dados pessoais/empresariais.
- Ao contribuir, não faça commit de caminhos absolutos de máquinas, nomes de usuário
  ou qualquer documento real extraído do diário.
