import dbf

# --- CRIA E SALVA O ARQUIVO DBF ---
def salvar_em_dbf(produtos, caminho_arquivo):
    table = dbf.Table(
        caminho_arquivo,
        'EAN C(20); PRODUTO C(50); APRESEN C(50); PF N(10,2); PMC N(10,2)',
        codepage='cp1252',
        dbf_type='db3'
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