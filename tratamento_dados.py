import pandas as pd

def remover_duplicadas(dados: pd.DataFrame) -> pd.DataFrame:
    num_duplicatas = dados.duplicated().sum()
    
    if num_duplicatas > 0:
        print(f"\n---Removendo {num_duplicatas} linhas duplicadas ...")
        dados_sem_duplicatas = dados.drop_duplicates(keep='first').reset_index(drop=True)
        return dados_sem_duplicatas
    
    print("\n---Não foram encontradas linhas duplicadas.")
    return dados
    
def converter_tipos_colunas(dados: pd.DataFrame) -> pd.DataFrame:
    print("\n---Convertendo tipos de dados das colunas ...")
    
    colunas_numericas = ['Ano', 'Receita Total (receita bruta)', 'Lucro Líquido',
                         'Custo Operacional (OPEX)', 'Número de Funcionários']
    
    for coluna in colunas_numericas:
        if coluna in dados.columns:
            dados[coluna] = pd.to_numeric(dados[coluna], errors='coerce')
        else:
            print(f"\n---Coluna numérica '{coluna}' não encontrada")
    
    return dados

def tratar_dados_nulos(dados: pd.DataFrame) -> pd.DataFrame:
    print("\n---Tratando dados nulos/em branco ...")
    
    colunas_numericas = dados.select_dtypes(include=['number']).columns
    dados[colunas_numericas] = dados[colunas_numericas].fillna(0)

    colunas_texto = dados.select_dtypes(include=['object']).columns
    dados[colunas_texto] = dados[colunas_texto].fillna('Não Informado')

    colunas_inteiras = ['Ano', 'Número de Funcionários']
    for coluna in colunas_inteiras:
        if coluna in dados.columns:
            dados[coluna] = dados[coluna].astype(int)
    
    return dados

def padronizar_texto(dados: pd.DataFrame) -> pd.DataFrame:
    print("\n---Padronizando colunas de texto ...")

    colunas_para_padronizar = ['Empresa', 'País', 'Setor']
    for coluna in colunas_para_padronizar:
        dados[coluna] = dados[coluna].str.title()
    
    return dados

def pipeline_tratamento(dados: pd.DataFrame) -> pd.DataFrame:
    
    if dados is None:
        return None
    
    print("\n---Iniciando pipeline de tratamento de dados---")
    dados_tratados = dados.copy()
    dados_tratados = converter_tipos_colunas(dados_tratados)
    dados_tratados = tratar_dados_nulos(dados_tratados)
    dados_tratados = padronizar_texto(dados_tratados)
    dados_tratados = remover_duplicadas(dados_tratados)
    return dados_tratados