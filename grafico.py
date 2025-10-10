"""
Módulo de Geração de Gráficos

Este módulo utiliza a biblioteca Matplotlib para criar visualizações dos dados
tabulares tratados. As funções aqui geram gráficos de barras e os salvam
como arquivos de imagem .png.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

def criar_e_salvar_grafico_barras(dados: pd.DataFrame, eixo_x: str, eixo_y: str, titulo: str, pasta_saida: str):
    """
    Cria e salva um único gráfico de barras como um arquivo de imagem (.png)
    """
    # Se não houver dados, não faz nada.
    if dados is None or dados.empty:
        print(f"   - Aviso: Não há dados para gerar o gráfico '{titulo}'.")
        return

    print(f"   - Gerando e salvando gráfico: '{titulo}'...")
    
    try:
        # Garante que a pasta de saída para os gráficos exista
        os.makedirs(pasta_saida, exist_ok=True)

        # Ordena os dados pelo eixo Y em ordem decrescente para um melhor visual
        dados_ordenados = dados.sort_values(by=eixo_y, ascending=False)

        # Cria uma nova figura/gráfico com um tamanho específico
        plt.figure(figsize=(12, 7))
        
        # Plota os dados como um gráfico de barras
        plt.bar(dados_ordenados[eixo_x], dados_ordenados[eixo_y], edgecolor='black')
        
        # Define os textos do gráfico (título, rótulos dos eixos)
        plt.title(titulo, fontsize=16)
        plt.xlabel(eixo_x, fontsize=12)
        plt.ylabel(eixo_y, fontsize=12)
       
        # Rotaciona os rótulos do eixo X para evitar sobreposição
        plt.xticks(rotation=45, ha='right')
       
        # Adiciona uma grade horizontal para facilitar a leitura
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Ajusta o layout para garantir que nada seja cortado
        plt.tight_layout()
        
        # Cria um nome de arquivo a partir do título do gráfico
        nome_arquivo = f"{titulo.lower().replace(' ', '_')}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        
        # Salva a figura gerada no caminho especificado
        plt.savefig(caminho_completo)
        
        # Fecha a figura salva
        plt.close()
        
        print(f"     -> Gráfico salvo em '{caminho_completo}'")

    except Exception as e:
        print(f"   - ERRO ao gerar o gráfico '{titulo}': {e}")


def gerar_todos_graficos(dados: pd.DataFrame):
    """
    Orquestra a criação de todos os gráficos de análise definidos.
    """
    # Se não houver dados, interrompe o processo
    if dados is None:
        print("\n--- Análise gráfica interrompida: DataFrame está vazio. ---")
        return

    # Define o caminho para a pasta de saída dos gráficos de forma segura
    CAMINHO_BASE_DO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
    PASTA_GRAFICOS = os.path.join(CAMINHO_BASE_DO_SCRIPT, "saida_graficos")

    print(f"\n--- Iniciando geração de gráficos (salvando em '{PASTA_GRAFICOS}') ---")
    
    # Agrupa os dados por empresa e soma os valores numéricos
    dados_por_empresa = dados.groupby('Empresa').sum(numeric_only=True).reset_index()
    
    # Chama a função de criação de gráficos para cada análise de empresa
    criar_e_salvar_grafico_barras(dados_por_empresa, 'Empresa', 'Receita Total (receita bruta)', 'Receita Total por Empresa', PASTA_GRAFICOS)
    criar_e_salvar_grafico_barras(dados_por_empresa, 'Empresa', 'Lucro Líquido', 'Lucro Líquido por Empresa', PASTA_GRAFICOS)
    
    # Agrupa os dados por país e soma os valores numéricos
    dados_por_pais = dados.groupby('País').sum(numeric_only=True).reset_index()

    # Chama a função de criação de gráficos para cada análise de país
    criar_e_salvar_grafico_barras(dados_por_pais, 'País', 'Receita Total (receita bruta)', 'Receita Total por País', PASTA_GRAFICOS)
    criar_e_salvar_grafico_barras(dados_por_pais, 'País', 'Lucro Líquido', 'Lucro Líquido por País', PASTA_GRAFICOS)
    
    print("--- Geração de gráficos finalizada ---")