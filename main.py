import functions as fc


print('---------------- INICIANDO PIPELINE ----------------')

if __name__ == "__main__":
    nome_do_arquivo = input("Digite o nome do arquivo (com extensão) que deseja ler: ")

    if not nome_do_arquivo.strip():
        print("\n--- ERRO: Nenhum nome de arquivo foi digitado.")
    else:
        dados = fc.carregar_dados(nome_do_arquivo)
    
    if dados is not None:
        print("\n--- Dados Extraídos ---")
        print(dados)
        print("\n--- Informações do DataFrame ---")
        dados.info()
    else:
        print("\n---Não foi possível carregar os dados.")