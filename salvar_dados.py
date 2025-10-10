"""
Módulo de Salvamento de Dados (Carregamento)

Este módulo contém as funções para persistir os dados processados em disco.
Ele lida com o salvamento de dados em forma de tabela, no formato .csv, e dados de texto, no formato .json
"""

import pandas as pd
import json
import os

def salvar_tabela_como_csv(dados: pd.DataFrame, caminho_saida: str):
    """
    Salva um DataFrame em um arquivo no formato .csv
    """
    # Verifica se os dados estiverem vazios
    if dados is None:
        print("   - AVISO: Nenhum dado de tabela para salvar.")
        return

    print(f"   - Salvando tabela tratada em '{caminho_saida}'...")
    try:
        # Garante que a pasta de destino exista antes de tentar salvar.
        os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
        
        # 'index=False' impede o Pandas de salvar o índice do DataFrame como uma coluna no CSV
        # 'encoding='utf-8-sig'' garante a compatibilidade com acentos e caracteres especiais ao abrir o arquivo no Excel
        dados.to_csv(caminho_saida, index=False, encoding='utf-8-sig')
        print(f"     -> Tabela salva com sucesso.")
        
    except Exception as e:
        print(f"   - ERRO ao salvar o arquivo CSV: {e}")


def salvar_texto_como_json(dados_para_salvar: dict, caminho_saida: str):
    """
    Salva um dicionário de dados em um arquivo no formato .json.
    """
    # Não faz nada se o dicionário estiver vazio
    if not dados_para_salvar:
        print("   - AVISO: Nenhum dado de texto para salvar.")
        return

    print(f"   - Salvando dados de texto em '{caminho_saida}'...")
    try:
        # Garante a existência do diretório
        os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
        
        # Abre o arquivo em modo de escrita ('w') com a codificação UTF-8.
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            # 'json.dump' escreve o dicionário no arquivo.
            # 'ensure_ascii=False' permite que caracteres acentuados sejam salvos corretamente.
            # 'indent=4' formata o JSON de forma legível, com 4 espaços de indentação.
            json.dump(dados_para_salvar, f, ensure_ascii=False, indent=4)
        print(f"     -> Arquivo JSON salvo com sucesso.")
        
    except Exception as e:
        print(f"   - ERRO ao salvar o arquivo JSON: {e}")