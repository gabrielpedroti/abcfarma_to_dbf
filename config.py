from dotenv import load_dotenv
import os

load_dotenv()

# --- CONFIGURAÇÕES DO USUÁRIO ---
CNPJ_ASSOCIADO = os.getenv('CNPJ_ASSOCIADO')
SENHA_ASSOCIADO = os.getenv('SENHA_ASSOCIADO')
CNPJ_SOFTWARE = os.getenv('CNPJ_SOFTWARE')
INCLUIR_PMC_ZERADO = True

# --- ENDPOINTS DA API ABCFARMA ---
URL_DADOS = 'https://webserviceabcfarma.org.br/webservice/'
URL_INFO = 'https://webserviceabcfarma.org.br/webservice/info/'