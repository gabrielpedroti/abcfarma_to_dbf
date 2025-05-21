import requests
from config import CNPJ_ASSOCIADO, SENHA_ASSOCIADO, CNPJ_SOFTWARE, URL_INFO, URL_DADOS
from utils.logger import salvar_log
from datetime import datetime

# --- BUSCA DATA DE ATUALIZAÇÃO ---
def buscar_data_atualizacao():
    payload = {
        'cnpj_sh': CNPJ_SOFTWARE,
        'cnpj_cpf': CNPJ_ASSOCIADO,
        'senha': SENHA_ASSOCIADO
    }
    try:
        response = requests.post(URL_INFO, data=payload, timeout=15)
        response.raise_for_status()
        json_resp = response.json()

        if json_resp.get('status') == 'error':
            mensagem = f"[ERRO] Código {json_resp.get('error_code')} - {json_resp.get('error_message')}"
            salvar_log(mensagem)
            return 'sem_data'

        raw_data = json_resp.get('data_atualizacao', '')
        return datetime.strptime(raw_data.split()[0], '%Y-%m-%d').strftime('%d-%m-%Y') if raw_data else 'sem_data'
    except Exception as e:
        salvar_log(f"[ERRO] Falha ao obter data de atualização: {e}")
        return 'sem_data'

# --- BUSCA UMA PÁGINA DE PRODUTOS ---
def buscar_pagina_abcfarma(pagina):
    payload = {
        'cnpj_cpf': CNPJ_ASSOCIADO,
        'senha': SENHA_ASSOCIADO,
        'cnpj_sh': CNPJ_SOFTWARE,
        'pagina': pagina
    }
    try:
        response = requests.post(URL_DADOS, data=payload, timeout=30)
        response.raise_for_status()
        json_resp = response.json()

        if json_resp.get('status') == 'error':
            mensagem = f"[ERRO] Código {json_resp.get('error_code')} - {json_resp.get('error_message')}"
            salvar_log(mensagem)
            raise Exception(mensagem)

        return json_resp
    except Exception as e:
        salvar_log(f"[ERRO] Falha ao obter página {pagina}: {e}")
        return None