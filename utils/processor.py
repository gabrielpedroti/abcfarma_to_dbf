from config import INCLUIR_PMC_ZERADO

# --- PROCESSA JSON EM LISTA DE PRODUTOS ---
def processar_dados(dados_json):
    produtos = []
    todos = dados_json.get('data', [])
    for item in todos:
        pmc_valor = item.get('PMC_18', '')
        pmc_valor_float = float(pmc_valor) if pmc_valor else 0.0

        if not INCLUIR_PMC_ZERADO and pmc_valor_float == 0.0:
            continue

        produtos.append({
            'EAN': item.get('EAN', ''),
            'PRODUTO': item.get('NOME', ''),
            'APRESENTACAO': item.get('DESCRICAO', ''),
            'PF': item.get('PF_18', ''),
            'PMC': item.get('PMC_18', '')
        })

    return produtos, len(todos)