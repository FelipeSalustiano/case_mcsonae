import os
import pandas as pd
import matplotlib.pyplot as plt

def criar_e_salvar_grafico_barras(dados: pd.DataFrame, eixo_x: str, eixo_y: str, titulo: str, pasta_saida: str):
    """
    Cria e SALVA um gráfico de barras como um arquivo de imagem (.png) usando Matplotlib.
    """
    if dados is None or dados.empty:
        print(f"   - Aviso: Não há dados para gerar o gráfico '{titulo}'.")
        return

    print(f"   - Gerando e salvando gráfico: '{titulo}'...")
    try:
        # Garante que a pasta de saída exista
        if not os.path.exists(pasta_saida):
            os.makedirs(pasta_saida)

        # Ordena os dados para um gráfico mais legível
        dados_ordenados = dados.sort_values(by=eixo_y, ascending=False)

        # --- Comandos do Matplotlib ---
        
        # 1. Cria uma tela em branco para o gráfico
        plt.figure(figsize=(12, 7))
        
        # 2. Plota o gráfico de barras
        plt.bar(dados_ordenados[eixo_x], dados_ordenados[eixo_y])
        
        # 3. Adiciona título e rótulos aos eixos
        plt.title(titulo, fontsize=16)
        plt.xlabel(eixo_x, fontsize=12)
        plt.ylabel(eixo_y, fontsize=12)
        
        # 4. Gira os rótulos do eixo X para evitar que se sobreponham
        plt.xticks(rotation=45, ha='right')
        
        # 5. Adiciona uma grade para facilitar a leitura
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # 6. Ajusta o layout para garantir que nada seja cortado
        plt.tight_layout()
        
        # 7. Salva a figura em um arquivo de imagem
        nome_arquivo = f"{titulo.lower().replace(' ', '_')}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        plt.savefig(caminho_completo)
        
        # 8. Fecha a figura
        plt.close()
        
        print(f"     -> Gráfico salvo em '{caminho_completo}'")

    except Exception as e:
        print(f"   - ERRO ao gerar o gráfico '{titulo}': {e}")


def gerar_todos_graficos(dados: pd.DataFrame):
    """
    Orquestra a criação e salvamento de todos os gráficos de análise.
    """
    if dados is None:
        print("\n--- Análise gráfica interrompida: DataFrame está vazio. ---")
        return

    pasta_graficos = "saida_graficos"

    print(f"\n--- Iniciando geração de gráficos (salvando em '{pasta_graficos}') ---")
    
    # Agregando os dados por empresa antes de plotar
    dados_por_empresa = dados.groupby('Empresa').sum(numeric_only=True).reset_index()
    
    # Gráfico 1: Receita Total por Empresa
    criar_e_salvar_grafico_barras(dados_por_empresa, 'Empresa', 'Receita Total (receita bruta)', 'Receita Total por Empresa', pasta_graficos)

    # Gráfico 2: Lucro Líquido por Empresa
    criar_e_salvar_grafico_barras(dados_por_empresa, 'Empresa', 'Lucro Líquido', 'Lucro Líquido por Empresa', pasta_graficos)
    
    # Agrega os dados por país antes de plotar
    dados_por_pais = dados.groupby('País').sum(numeric_only=True).reset_index()

    # Gráfico 3: Receita Total por País
    criar_e_salvar_grafico_barras(dados_por_pais, 'País', 'Receita Total (receita bruta)', 'Receita Total por País', pasta_graficos)

    # Gráfico 4: Lucro Líquido por País
    criar_e_salvar_grafico_barras(dados_por_pais, 'País', 'Lucro Líquido', 'Lucro Líquido por País', pasta_graficos)
    
    print("--- Geração de gráficos finalizada ---")