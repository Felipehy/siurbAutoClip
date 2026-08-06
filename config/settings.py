import os
import dotenv

# Diretório raiz do projeto (este arquivo fica em config/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carrega as variáveis de ambiente a partir do .env
# O caminho do .env pode ser sobrescrito pela variável PATH_ENV.
PATH_ENV = os.getenv("PATH_ENV", os.path.join(BASE_DIR, ".env"))
dotenv.load_dotenv(PATH_ENV)

# Caminhos de arquivos/binários (todos configuráveis via .env).
# Por padrão são resolvidos de forma relativa ao projeto, sem expor
# caminhos absolutos de nenhuma máquina específica.
PDF_PATH = os.getenv("PDF_PATH", os.path.join(BASE_DIR, "pdfs", "ContractAss.pdf"))
POPPLER = os.getenv("POPPLER_PATH", os.path.join(BASE_DIR, "poppler-25.12.0", "Library", "bin"))

# Caminho do executável do Tesseract. No Linux normalmente está no PATH
# (deixe vazio); no Windows aponte para o tesseract.exe via .env.
TESSERACT = os.getenv("TESSERACT_CMD")

# Banco de dados
HOST_DB = os.getenv("HOST_DB")
USER_DB = os.getenv("USER_DB")
PASSWD_DB = os.getenv("PASSWD_DB")

# URL do site de origem (Diário Oficial)
SITE_URL = os.getenv("SITE_URL")
