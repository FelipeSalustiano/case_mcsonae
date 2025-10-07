import pandas as pd
from manipulacao_arquivo import obter_extensao

# --- Funções de Salvamento Específicas ---

def salvar_como_csv(dados: pd.DataFrame, nome_arquivo_saida: str):
    try:
        dados.to_csv(nome_arquivo_saida, index=False, encoding='utf-8-sig')
        print(f"\n--- Dados salvos com sucesso em '{nome_arquivo_saida}' ---")
    except Exception as e:
        print(f"\n--- ERRO ao salvar o arquivo CSV: {e} ---")

def salvar_como_xlsx(dados: pd.DataFrame, nome_arquivo_saida: str):
    try:
        dados.to_excel(nome_arquivo_saida, index=False)
        print(f"\n--- Dados salvos com sucesso em '{nome_arquivo_saida}' ---")
    except Exception as e:
        print(f"\n--- ERRO ao salvar o arquivo Excel: {e} ---")

# --- FUNÇÃO DE ORQUESTRAÇÃO ---

def salvar_dados(dados: pd.DataFrame, nome_arquivo_saida: str):
    if dados is None:
        print("\n--- AVISO: Nenhum dado para salvar (DataFrame está vazio). ---")
        return

    extensao = obter_extensao(nome_arquivo_saida)

    funcoes_salvamento = {
        '.csv': salvar_como_csv,
        '.xlsx': salvar_como_xlsx
    }

    funcao = funcoes_salvamento.get(extensao)

    if funcao:
        funcao(dados, nome_arquivo_saida)
    else:
        print(f"\n--- ERRO: A extensão de saída '{extensao}' não é suportada. ---")