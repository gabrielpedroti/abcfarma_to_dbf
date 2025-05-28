from services.api import buscar_data_atualizacao, buscar_pagina_abcfarma
from services.dbf_service import salvar_em_dbf
from utils.processor import processar_dados
from utils.logger import salvar_log
from config import INCLUIR_PMC_ZERADO
from datetime import datetime

print("🔍 Buscando data de atualização da ABCFarma...")
data_formatada = buscar_data_atualizacao()
print(f"📅 Data da base: {data_formatada}")

pagina = 1
todos_produtos = []
total_produtos_recebidos = 0
total_com_pmc_valido = 0

print("\n📦 Iniciando coleta dos dados...")

while True:
    dados_json = buscar_pagina_abcfarma(pagina)
    if not dados_json:
        print("❌ Falha ao obter os dados. Verifique o log.")
        break

    produtos_filtrados, total_na_pagina = processar_dados(dados_json)
    todos_produtos.extend(produtos_filtrados)

    total_produtos_recebidos += total_na_pagina
    total_com_pmc_valido += len(produtos_filtrados)

    print(f"✅ Página {pagina} processada com {len(produtos_filtrados)} itens.")

    if pagina >= int(dados_json.get('total_paginas', 1)):
        break
    pagina += 1

if todos_produtos:
    # Nome do arquivo: PRECO_ddmmaa.dbf
    data_compacta = datetime.now().strftime('%d%m%y')  # Exemplo: '190525'
    nome_arquivo = f"PRECO_{data_compacta}.dbf"

    salvar_em_dbf(todos_produtos, nome_arquivo)

    mensagem_sucesso = f"[SUCESSO] Arquivo gerado: {nome_arquivo}\nProdutos salvos: {len(todos_produtos)}"
    salvar_log(mensagem_sucesso)

    resumo = f"""
[RESUMO]
Total recebido da ABCFarma: {total_produtos_recebidos}
Total com PMC > 0: {total_com_pmc_valido}
Produtos com PMC zerado salvos? {'NÃO' if not INCLUIR_PMC_ZERADO else 'SIM'}
"""
    salvar_log(resumo)
    print(f"\n🎉 {mensagem_sucesso}")
    print(resumo)

else:
    salvar_log("[ERRO] Nenhum produto foi salvo.")
    print("\n❌ Nenhum dado foi processado. Verifique o log.")