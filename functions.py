def tratamento_dados(arquivo):
    
    # Importando bibliotecas
    from time import sleep
    import pandas as pd

    # Iniciando função
    print('Iniciando o tratamento de dados...')
    sleep(3)

    print('------------- Tratando os dados -------------')
    df = pd.read_csv(arquivo, sep=',')

    # Tratamento de duplicatas
    df = df.drop_duplicates()
    print('Dados ducplicados removidos!')

    # Tratamento de nulos
    df['salario'] = pd.to_numeric(df['salario'].fillna('0'), errors='coerce')
    df['area_atuacao'] = df['area_atuacao'].fillna('Não preenchido')
    df['nome_funcionario'] = df['nome_funcionario'].fillna('Não preenchido')
    print('Dados nulos tratados!')

    # Tratamendo na coluna numérica
    df['salario'] = df['salario'].apply(lambda x: x if x > 0 else x * (-1))
    print('Dados numéricos tratados!')

    # Padronização dos dados categóricos
    df['nome_funcionario'] = df['nome_funcionario'].apply(lambda x: str(x).strip().upper())
    df['area_atuacao'] = df['area_atuacao'].apply(lambda x: str(x).strip().upper())
    print('Dados categóricos padronizados!')

    # Salvando arquivo tratado
    df.to_csv(f'dados_tratado.csv', index='False')

    print('Tratamento finalizado...')

