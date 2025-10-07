import pandas as pd

def sumario_executivo(dados: pd.DataFrame):
    if dados is None or dados.empty:
        print("\n--- Não há dados para gerar o sumário. ---")
        return

    print("\n" + "="*50)
    print(" " * 15 + "SUMÁRIO EXECUTIVO")
    print("="*50)

    try:
        # --- Cálculos ---
        colunas_financeiras = [
            'Receita Total (receita bruta)', 
            'Lucro Líquido'
        ]

        # 1. Cria uma lista vazia para armazenar as colunas que realmente existem.
        colunas_existentes = []
        
        # 2. Percorre a lista de colunas financeiras desejadas.
        for col in colunas_financeiras:
            # 3. Verifica se a coluna desejada está presente no DataFrame.
            if col in dados.columns:
                # 4. Se estiver, adiciona à lista de colunas existentes.
                colunas_existentes.append(col)
        
        # Calcula a soma apenas para as colunas que foram encontradas
        somas = dados[colunas_existentes].sum()

        # Conta o número de empresas únicas
        num_empresas = dados['Empresa'].nunique()
        
        # --- Exibição ---
        print(f"\nIndicadores Consolidados para {num_empresas} empresa(s):")
        
        # Mostra o resultado de cada coluna encontrada
        for nome_coluna, total in somas.items():
            # Formata o print para alinhar os valores
            print(f"  - {nome_coluna:<30}: € {total:,.2f}")
            
    except Exception as e:
        print(f"\n--- ERRO ao gerar o sumário executivo: {e} ---")
    
    finally:
        print("="*50)