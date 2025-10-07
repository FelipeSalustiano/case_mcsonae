from manipulacao_arquivo import carregar_dados
from tratamento_dados import pipeline_tratamento
from salvar_dados import salvar_dados
from sumario import sumario_executivo
from grafico import gerar_todos_graficos

def main():
    """
    Função principal de todo o processo de ETL.
    """
    arquivo_para_ler = "base_empresas.docx" # ENTRADA MANUAL! Arquivo que será lido. Pode ser no formato PDF, CSV, XLSX e DOCX.
    
    # 1. EXTRAÇÃO (EXTRACT)
    df_bruto = carregar_dados(arquivo_para_ler)
    
    if df_bruto is None:
        print("\nProcesso interrompido devido a erro na leitura do arquivo.")
        return

    print("\n--- Amostra dos Dados Brutos ---")
    print(df_bruto.head())
    
    # 2. TRANSFORMAÇÃO (TRANSFORM)
    df_tratado = pipeline_tratamento(df_bruto)
    
    if df_tratado is None:
        print("\nProcesso interrompido durante o tratamento dos dados.")
        return

    print("\n--- Amostra dos Dados Tratados ---")
    print(df_tratado.head())
    print("\n--- Informações do DataFrame Tratado ---")
    df_tratado.info()

    # 3. GERAÇÃO DOS GRÁFICOS
    gerar_todos_graficos(df_tratado)

    # 4. IMPRESSÃO DO SUMÁRIO
    sumario_executivo(df_tratado)
    
    # 4. CARREGAMENTO (LOAD)
    nome_arquivo_final = "empresas_tratado_final.xlsx" # ENTRADA MANUAL! Pode ser salvo no padrão CSV (.csv) ou XLSX (.xlsx)
    salvar_dados(df_tratado, nome_arquivo_final)

if __name__ == "__main__":
    main()