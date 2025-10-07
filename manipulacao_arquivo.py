import os
import pdfplumber
import pandas as pd
from docx import Document

# --- Funções de Leitura Específicas ---

def obter_extensao(nome_arquivo: str) -> str:
    _ , extensao = os.path.splitext(nome_arquivo)
    return extensao.lower()

def ler_pdf(nome_arquivo: str) -> pd.DataFrame:
    print(f"\n---Iniciando a leitura do arquivo PDF: '{nome_arquivo}'...")
    try:
        with pdfplumber.open(nome_arquivo) as pdf:
            if not pdf.pages:
                print("\n--- AVISO: O arquivo PDF está vazio (não contém páginas).")
                return None
            
            primeira_pagina = pdf.pages[0]
            tabelas = primeira_pagina.extract_tables()

            if not tabelas:
                print("\n---AVISO: Nenhuma tabela foi encontrada na primeira página.")
                return None

            # Processa apenas a primeira tabela encontrada
            primeira_tabela = tabelas[0]

            if not primeira_tabela or len(primeira_tabela) < 1:
                print("\n--- AVISO: A tabela encontrada no PDF está vazia.")
                return None

            df = pd.DataFrame(primeira_tabela[1:], columns=primeira_tabela[0])
            print("\n---Leitura do PDF concluída com sucesso.")
            return df

    except Exception as e:
        # Captura outras possíveis exceções
        print(f"\n---ERRO ao processar o PDF: {e}")
        return None

def ler_csv(nome_arquivo: str) -> pd.DataFrame:
    print(f"\n---Iniciando a leitura do arquivo CSV: '{nome_arquivo}'...")
    try:
        df = pd.read_csv(nome_arquivo)
        print("\n---Leitura do CSV concluída com sucesso.")
        return df
    except FileNotFoundError:
        print(f"\n---ERRO: O arquivo '{nome_arquivo}' não foi encontrado!")
        return None
    except Exception as e:
        print(f"\n---ERRO ao ler o arquivo CSV: {e}")
        return None

def ler_docx(nome_arquivo: str) -> pd.DataFrame:
    print(f"\n---Iniciando a leitura do arquivo DOCX: {nome_arquivo} ...")
    try:
        lista_tabelas = Document(nome_arquivo).tables
        if not lista_tabelas:
            print(f"\nArquivo {nome_arquivo} está vazio ou não possui tabelas!")
            return None
        
        primeira_tabela = lista_tabelas[0]
        tabela_completa = []
        
        for linha in primeira_tabela.rows:
            texto_linha = []
            for celula in linha.cells:
                texto_linha.append(celula.text)
            tabela_completa.append(texto_linha)
        
        if not tabela_completa or len(tabela_completa) < 1:
            print(f"\n---ERRO: Tabela do arquivo {nome_arquivo} está vazia!")
            return None
        
        df = pd.DataFrame(tabela_completa[1:], columns=tabela_completa[0])
        print("\n--- Leitura do DOCX concluída com sucesso!")
        return df

    except FileNotFoundError:
        print(f"\n---ERRO: O arquivo '{nome_arquivo}' não foi encontrado!")
        return None
    except Exception as e:
        # Captura erros de parsing, encoding etc.
        print(f"\n---ERRO ao ler o arquivo DOCX: {e}")
        return None

def ler_xlsx(nome_arquivo: str) -> pd.DataFrame:
    """Lê a primeira aba de um arquivo XLSX (Excel) e a retorna como um DataFrame."""
    print(f"\n---Iniciando a leitura do arquivo XLSX: '{nome_arquivo}'...")
    try:
        df = pd.read_excel(nome_arquivo)
        print("\n---Leitura do XLSX concluída com sucesso.")
        return df
    except FileNotFoundError:
        print(f"\n---ERRO: O arquivo '{nome_arquivo}' não foi encontrado!")
        return None
    except Exception as e:
        print(f"\n---ERRO ao ler o arquivo XLSX: {e}")
        return None

# --- Função Principal de Orquestração ---

def carregar_dados(nome_arquivo: str) -> pd.DataFrame:
    
    extensao = obter_extensao(nome_arquivo)

    # Usando um dicionário para selecionar a função.
    funcoes_leitura = {
        '.pdf': ler_pdf,
        '.csv': ler_csv,
        '.docx': ler_docx,
        '.xlsx': ler_xlsx
    }

    # Procura a função no dicionário usando a extensão
    funcao = funcoes_leitura.get(extensao)

    if funcao:
        return funcao(nome_arquivo)
    else:
        print(f"\n---ERRO: A extensão '{extensao}' não é suportada.")
        return None