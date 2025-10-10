"""
Módulo Principal

Este script é o ponto de entrada do programa. Ele é responsável por:
1. Definir as pastas de entrada e saída de forma segura, baseando-se na localização do próprio script
2. Escanear a pasta de entrada em busca de arquivos para processar
3. Para cada arquivo encontrado, determinar o tipo de processamento necessário com base na sua extensão
4. Chamar as funções de processamento específicas para tabelas (.csv, .xlsx) ou para textos (.pdf, .docx)
"""

import os
from manipulacao_arquivo import extrair_tabela, extrair_texto
from tratamento_dados import pipeline_tratamento
from tratamento_texto import limpar_texto, gerar_estatisticas_texto
from salvar_dados import salvar_tabela_como_csv, salvar_texto_como_json
from sumario import sumario_executivo
from grafico import gerar_todos_graficos

CAMINHO_BASE_DO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_ENTRADA = os.path.join(CAMINHO_BASE_DO_SCRIPT, "entrada")
PASTA_SAIDA = os.path.join(CAMINHO_BASE_DO_SCRIPT, "saida")


def processar_arquivo_tabela(caminho_arquivo: str, nome_arquivo: str):
    """
    Executa a pipeline completa para arquivos de tabela (CSV, XLSX).
    """
    # Etapa 1: Extrair os dados brutos da tabela do arquivo
    dado_bruto = extrair_tabela(caminho_arquivo)
    
    # Se a extração falhar, retorna None e interrompe a função
    if dado_bruto is None:
        return

    # Etapa 2: Aplicar todo o pipeline de tratamento e limpeza dos dados
    dado_tratado = pipeline_tratamento(dado_bruto)

    # Se o tratamento falhar, interrompe a função
    if dado_tratado is None:
        return
        
    # Etapa 3: Gera e salva os gráficos com base nos dados tratados
    gerar_todos_graficos(dado_tratado)

    # Etapa 4: Preparar o nome e o caminho do arquivo de saída
    nome_base, _ = os.path.splitext(nome_arquivo)
    nome_saida_csv = f"{nome_base}_tratado.csv"
    caminho_saida_csv = os.path.join(PASTA_SAIDA, nome_saida_csv)
    
    # Etapa 5: Salvar o DataFrame tratado no novo arquivo CSV
    salvar_tabela_como_csv(dado_tratado, caminho_saida_csv)

    # Imprime o sumário dos indicadores financeiros
    sumario_executivo(dado_tratado)


def processar_arquivo_texto(caminho_arquivo: str, nome_arquivo: str):
    """
    Executa a pipeline completa para arquivos de texto (PDF, DOCX)
    """
    
    # Etapa 1: Extrair o texto do arquivo como uma lista de parágrafos
    lista_paragrafos_brutos = extrair_texto(caminho_arquivo)
    
    if not lista_paragrafos_brutos:
        print("   - Falha ao extrair texto ou arquivo sem conteúdo. Pulando para o próximo arquivo.")
        return

    # Etapa 2: Limpar cada parágrafo individualmente
    print("   - Limpando cada parágrafo extraído...")
    paragrafos_limpos = []
    for p in lista_paragrafos_brutos:
        paragrafo_processado = limpar_texto(p)
        paragrafos_limpos.append(paragrafo_processado)

    paragrafos_realmente_limpos = []
    for p in paragrafos_limpos:
        if p:
            paragrafos_realmente_limpos.append(p)
    paragrafos_limpos = paragrafos_realmente_limpos

    # Etapa 3: Gerar estatísticas a partir do texto completo
    print("   - Gerando estatísticas gerais do texto...")
    texto_completo_limpo = " ".join(paragrafos_limpos)
    estatisticas = gerar_estatisticas_texto(texto_completo_limpo)

    # Etapa 4: Montar a estrutura do dicionário para salvar no JSON
    dados_finais = {
        "estatisticas_gerais": estatisticas,
        "paragrafos_limpos": paragrafos_limpos
    }
    
    # Etapa 5: Preparar o nome e o caminho do arquivo de saída JSON
    nome_base, _ = os.path.splitext(nome_arquivo)
    nome_saida_json = f"{nome_base}_texto.json"
    caminho_saida_json = os.path.join(PASTA_SAIDA, nome_saida_json)
    
    # Etapa 6: Salvar o dicionário final no novo arquivo JSON
    salvar_texto_como_json(dados_finais, caminho_saida_json)

def main():
    """
    Função principal que inicia e gerencia todo o processo
    """
    print("="*60)
    print(" " * 20 + "INICIANDO PROCESSAMENTO")
    print("="*60)

    os.makedirs(PASTA_ENTRADA, exist_ok=True)
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    
    try:
        lista_arquivos = os.listdir(PASTA_ENTRADA)
        if not lista_arquivos:
            print(f"\nAVISO: A pasta '{PASTA_ENTRADA}' está vazia.")
            return
            
    except FileNotFoundError:
        print(f"ERRO: A pasta de entrada '{PASTA_ENTRADA}' não foi encontrada!")
        return
        
    print(f"\nEncontrados {len(lista_arquivos)} arquivo(s) na pasta de entrada.")
    
    for nome_arquivo in lista_arquivos:
        caminho_completo = os.path.join(PASTA_ENTRADA, nome_arquivo)
        _, extensao = os.path.splitext(nome_arquivo)
        extensao = extensao.lower()

        print(f"\n--- Processando arquivo: '{nome_arquivo}' ---")

        if extensao in ['.csv', '.xlsx']:
            processar_arquivo_tabela(caminho_completo, nome_arquivo)
        
        elif extensao in ['.pdf', '.docx']:
            processar_arquivo_texto(caminho_completo, nome_arquivo)
            
        else:
            print(f"   - AVISO: Extensão '{extensao}' não suportada.")

    print("\n" + "="*60)
    print(" " * 17 + "PROCESSAMENTO FINALIZADO")
    print("="*60)


if __name__ == "__main__":
    main()