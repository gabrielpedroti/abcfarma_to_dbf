import requests
import dbf
import json
from datetime import datetime

# Buscando dados da URL com exemplo da ABCFarma
def buscar_dados_abcfarma():
    url = 'https://webserviceabcfarma.org.br/webservice/exemplo/2025'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Erro ao buscar dados: {response.status_code}')

# Processando os dados e mapeando os campos
def processar_dados(dados_json):
    produtos = []
    for item in dados_json['data']:
        produtos.append({
            'EAN': item.get('EAN', ''),
            'PRODUTO': item.get('NOME', ''),
            'APRESENTACAO': item.get('DESCRICAO', ''),
            'PF': item.get('PF_18', ''),
            'PMC': item.get('PMC_18', '')
        })
    return produtos

# Criar e salvar o DBF com compatibilidade total
def salvar_em_dbf(produtos, caminho_arquivo):
    table = dbf.Table(
        caminho_arquivo,
        'EAN C(20); PRODUTO C(50); APRESEN C(50); PF N(10,2); PMC N(10,2)',
        codepage='cp1252',  # Compatível com Windows / Access 2003
        dbf_type='db3'      # Forçar DBase III
    )
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

# MAIN
if __name__ == "__main__":
    dados_json = buscar_dados_abcfarma()
    produtos = processar_dados(dados_json)

    # Nome curto com data
    data_compacta = datetime.now().strftime('%d%m%y')
    nome_arquivo = f"PRECO_{data_compacta}.dbf"

    salvar_em_dbf(produtos, nome_arquivo)
    print(f"🎉 Arquivo DBF gerado com sucesso: {nome_arquivo}")