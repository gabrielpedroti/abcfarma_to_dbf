from services.api import buscar_data_atualizacao, buscar_pagina_abcfarma
from services.dbf_service import salvar_em_dbf
from utils.processor import processar_dados
from utils.logger import salvar_log

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
    nome_arquivo = f"atualizacao_precos_abcfarma_{data_formatada}.dbf"
    salvar_em_dbf(todos_produtos, nome_arquivo)

    mensagem_sucesso = f"[SUCESSO] Arquivo gerado: {nome_arquivo}\nProdutos salvos: {len(todos_produtos)}"
    salvar_log(mensagem_sucesso)

    resumo = f"""
[RESUMO]
Total recebido da ABCFarma: {total_produtos_recebidos}
Total com PMC > 0: {total_com_pmc_valido}
Filtro PMC zerado ativado? {'NÃO' if not INCLUIR_PMC_ZERADO else 'SIM'}
"""
    salvar_log(resumo)
    print(f"\n🎉 {mensagem_sucesso}")
    print(resumo)
else:
    salvar_log("[ERRO] Nenhum produto foi salvo.")
    print("\n❌ Nenhum dado foi processado. Verifique o log.")