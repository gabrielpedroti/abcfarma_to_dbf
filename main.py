import requests
import dbf
from datetime import datetime

# --- CONFIGURAÇÕES DO USUÁRIO ---
CNPJ_ASSOCIADO = '00000000000000'
SENHA_ASSOCIADO = 'sua_senha_aqui'
CNPJ_SOFTWARE = '00000000000000'

# --- ENDPOINTS DA API ABCFARMA ---
URL_DADOS = 'https://webserviceabcfarma.org.br/webservice/'
URL_INFO = 'https://webserviceabcfarma.org.br/webservice/info/'

# --- SALVA LOG EM ARQUIVO TXT ---
def salvar_log(mensagem):
    with open("log_execucao.txt", "a", encoding="utf-8") as log:
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        log.write(f"{timestamp} - {mensagem}\n")

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

# --- PROCESSA JSON EM LISTA DE PRODUTOS ---
def processar_dados(dados_json):
    produtos = []
    for item in dados_json.get('data', []):
        produtos.append({
            'EAN': item.get('EAN', ''),
            'PRODUTO': item.get('NOME', ''),
            'APRESENTACAO': item.get('DESCRICAO', ''),
            'PF': item.get('PF_18', ''),
            'PMC': item.get('PMC_18', '')
        })
    return produtos

# --- CRIA E SALVA O ARQUIVO DBF ---
def salvar_em_dbf(produtos, caminho_arquivo):
    table = dbf.Table(caminho_arquivo,
        'EAN C(20); PRODUTO C(100); APRESEN C(100); PF N(10,2); PMC N(10,2)')
    table.open(mode=dbf.READ_WRITE)

    for produto in produtos:
        table.append((
            produto['EAN'],
            produto['PRODUTO'],
            produto['APRESENTACAO'],
            float(produto['PF']) if produto['PF'] else 0.0,
            float(produto['PMC']) if produto['PMC'] else 0.0
        ))

    table.close()

# --- FUNÇÃO PRINCIPAL ---
if __name__ == "__main__":
    print("🔍 Buscando data de atualização da ABCFarma...")
    data_formatada = buscar_data_atualizacao()
    print(f"📅 Data da base: {data_formatada}")

    pagina = 1
    todos_produtos = []

    print("\n📦 Iniciando coleta dos dados...")
    while True:
        dados_json = buscar_pagina_abcfarma(pagina)
        if not dados_json:
            print("❌ Falha ao obter os dados. Verifique o log.")
            break

        produtos = processar_dados(dados_json)
        todos_produtos.extend(produtos)

        print(f"✅ Página {pagina} processada com {len(produtos)} itens.")

        if pagina >= int(dados_json.get('total_paginas', 1)):
            break
        pagina += 1

    if todos_produtos:
        nome_arquivo = f"atualizacao_precos_abcfarma_{data_formatada}.dbf"
        salvar_em_dbf(todos_produtos, nome_arquivo)

        mensagem_sucesso = f"[SUCESSO] Arquivo gerado: {nome_arquivo}\nProdutos salvos: {len(todos_produtos)}"
        salvar_log(mensagem_sucesso)

        print(f"\n🎉 {mensagem_sucesso}")
    else:
        salvar_log("[ERRO] Nenhum produto foi salvo.")
        print("\n❌ Nenhum dado foi processado. Verifique o log.")