"""
Módulo de Tratamento de Dados de Tabela

Este módulo contém todas as funções necessárias para limpar e transformar os dados
extraídos em formato de tabela (DataFrame do Pandas).
As operações incluem remoção de duplicatas, conversão de tipos,
tratamento de valores nulos e padronização de textos.
"""

import pandas as pd

def remover_duplicadas(dados: pd.DataFrame) -> pd.DataFrame:
    """
    Verifica e remove linhas duplicadas de um DataFrame.
    """
    # Conta o número de linhas que são duplicatas exatas.
    num_duplicatas = dados.duplicated().sum()
    
    # Se encontrar uma ou mais duplicatas
    if num_duplicatas > 0:
        print(f"\n---Removendo {num_duplicatas} linhas duplicadas ...")
        # Remove as duplicatas, mantendo a primeira ocorrência e rearruma o índice do DataFrame após a remoção
        dados_sem_duplicatas = dados.drop_duplicates(keep='first').reset_index(drop=True)
        return dados_sem_duplicatas
    # Caso contrário
    else:
        print("\n---Não foram encontradas linhas duplicadas.")
        return dados
    
def converter_tipos_colunas(dados: pd.DataFrame) -> pd.DataFrame:
    """
    Converte colunas específicas para o tipo numérico.
    """
    print("\n---Convertendo tipos de dados das colunas ...")
    
    # Lista de colunas que esperamos que sejam numéricas
    colunas_numericas = ['Ano', 'Receita Total (receita bruta)', 'Lucro Líquido',
                         'Custo Operacional (OPEX)', 'Número de Funcionários']
    
    # Varr cada nome de coluna na lista.
    for coluna in colunas_numericas:
        # Verifica se a coluna realmente existe no DataFrame.
        if coluna in dados.columns:
            # Converte a coluna para tipo numérico
            # 'errors=coerce' força valores que não podem ser convertidos a se tornarem 'NaN' (Not a Number)
            dados[coluna] = pd.to_numeric(dados[coluna], errors='coerce')
        else:
            # Se a coluna não for encontrada, imprime um aviso
            print(f"\n---Coluna numérica '{coluna}' não encontrada")
    
    return dados

def tratar_dados_nulos(dados: pd.DataFrame) -> pd.DataFrame:
    """
    Preenche valores nulos (NaN) em colunas numéricas e de texto
    """
    print("\n---Tratando dados nulos/em branco ...")
    
    # Para colunas numéricas, preenche os valores nulos com 0
    colunas_numericas = dados.select_dtypes(include=['number']).columns
    dados[colunas_numericas] = dados[colunas_numericas].fillna(0)

    # Para colunas de texto, preenche os valores nulos com 'Não Informado'
    colunas_texto = dados.select_dtypes(include=['object']).columns
    dados[colunas_texto] = dados[colunas_texto].fillna('Não Informado')

    # Garante que colunas que devem ser inteiras (sem casas decimais) sejam convertidas
    colunas_inteiras = ['Ano', 'Número de Funcionários']
    for coluna in colunas_inteiras:
        if coluna in dados.columns:
            dados[coluna] = dados[coluna].astype(int)
    
    return dados

def padronizar_texto(dados: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza o texto de colunas específicas para o formato "Title Case" - Primeira letra maiúscula e o resto minúscula
    """
    print("\n---Padronizando colunas de texto ...")

    # Lista de colunas de texto a serem padronizadas.
    colunas_para_padronizar = ['Empresa', 'País', 'Setor']
    for coluna in colunas_para_padronizar:
        dados[coluna] = dados[coluna].str.title()
    
    return dados

def pipeline_tratamento(dados: pd.DataFrame) -> pd.DataFrame:
    """
    Orquestra a execução de todas as funções de tratamento em sequência.
    """
    # Caso de um DataFrame vazio seja passado
    if dados is None:
        return None
    
    print("\n---Iniciando pipeline de tratamento de dados---")
    
    # Executa cada etapa do tratamento na ordem definida.
    dados_tratados = converter_tipos_colunas(dados)
    dados_tratados = tratar_dados_nulos(dados_tratados)
    dados_tratados = padronizar_texto(dados_tratados)
    dados_tratados = remover_duplicadas(dados_tratados)
    
    # Retorna o DataFrame final.
    return dados_tratados