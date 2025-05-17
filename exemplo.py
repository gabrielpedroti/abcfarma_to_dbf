import requests
import dbf
import json

# Função para buscar dados da ABCFarma
def buscar_dados_abcfarma():
    url = 'https://webserviceabcfarma.org.br/webservice/exemplo/2025'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Erro ao buscar dados: {response.status_code}')

# Função para processar os dados e fazer o mapeamento correto
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

# Função para criar e salvar o DBF
def salvar_em_dbf(produtos, caminho_arquivo):
    table = dbf.Table(caminho_arquivo, 
        'EAN C(20); PRODUTO C(100); APRESENTA C(100); PF N(10,2); PMC N(10,2)')
    table.open(mode=dbf.READ_WRITE)

    for produto in produtos:
        table.append((
            produto['EAN'],
            produto['PRODUTO'],
            produto['APRESENTACAO'],  # Pode manter assim, o valor é o mesmo, só o campo que foi renomeado
            float(produto['PF']) if produto['PF'] else 0.0,
            float(produto['PMC']) if produto['PMC'] else 0.0
        ))

    table.close()

# MAIN
if __name__ == "__main__":
    dados_json = buscar_dados_abcfarma()
    produtos = processar_dados(dados_json)
    salvar_em_dbf(produtos, 'precos_abcfarma.dbf')  # <<< AQUI FOI CORRIGIDO
    print('Arquivo DBF gerado com sucesso!')