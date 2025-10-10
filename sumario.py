"""
Módulo de Geração de Sumário Executivo

Este módulo é responsável por calcular e exibir um resumo dos principais
indicadores financeiros e operacionais das tabelas tratadas
"""

import pandas as pd

def sumario_executivo(dados: pd.DataFrame):
    """
    Calcula e imprime no console um sumário dos dados.
    """
    # Se não houver dados, imprime uma mensagem e encerra
    if dados is None or dados.empty:
        print("\n--- Não há dados para gerar o sumário. ---")
        return

    # Imprime um cabeçalho para o sumário
    print("\n" + "="*50)
    print(" " * 15 + "SUMÁRIO EXECUTIVO")
    print("="*50)

    try:
        # Lista de colunas financeiras que queremos somar.
        colunas_financeiras = [
            'Receita Total (receita bruta)', 
            'Lucro Líquido'
        ]

        # Verifica se uma coluna esperada (colunas_financeiras) existe no arquivo
        colunas_existentes = []
        for col in colunas_financeiras:
            if col in dados.columns:
                colunas_existentes.append(col)
        
        # Calcula a soma apenas para as colunas que foram encontradas
        somas = dados[colunas_existentes].sum()

        # Conta o número de valores únicos na coluna 'Empresa'
        num_empresas = dados['Empresa'].nunique()
        
        # Imprime o resumo dos resultados.
        print(f"Indicadores Consolidados para {num_empresas} empresa(s):")
        
        # Corre os resultados das somas para exibi-los.
        for nome_coluna, total in somas.items():
            # Formatação da string para alinhar os valores e formatar os números.
            # ':<30' alinha o texto à esquerda em um espaço de 30 caracteres.
            # ':,.2f' formata o número com separador de milhar e duas casas decimais
            print(f"  - {nome_coluna:<30}: € {total:,.2f}")
            
    except Exception as e:
        # Se ocorrer qualquer erro durante os cálculos, ele será capturado e exibido.
        print(f"\n--- ERRO ao gerar o sumário executivo: {e} ---")
    
    finally:
        # Este bloco é sempre executado, imprimindo o rodapé do sumário.
        print("="*50)