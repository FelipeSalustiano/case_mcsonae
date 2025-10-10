"""
Módulo de Manipulação de Arquivos (Extração)

Este módulo contém as funções responsáveis por ler os diferentes tipos de arquivos
(.csv, .xlsx, .pdf, .docx) e extrair seu conteúdo bruto.
Ele separa a lógica de extração de tabelas e de textos em funções diferentes.
"""

import os
import pdfplumber
import pandas as pd
from docx import Document

def extrair_tabela(caminho_arquivo: str) -> pd.DataFrame:
    """
    Extrai uma tabela de arquivos .csv ou .xlsx
    """
    print(f"   - Tentando extrair TABELA de '{os.path.basename(caminho_arquivo)}'...")
    
    # Extrai a extensão do arquivo para determinar como lê-lo
    _, extensao = os.path.splitext(caminho_arquivo)
    extensao = extensao.lower()

    # Bloco try/except para capturar possíveis erros durante a leitura do arquivo
    try:
        if extensao == '.csv':
            # Se for CSV, usa a função read_csv do Pandas.
            df = pd.read_csv(caminho_arquivo)
        elif extensao == '.xlsx':
            # Se for Excel, usa a função read_excel do Pandas.
            df = pd.read_excel(caminho_arquivo)
        else:
            # Se a extensão não for suportada para tabelas, informa e retorna None.
            print(f"   - ERRO: Extensão '{extensao}' não é suportada para extração de tabelas.")
            return None
        
        print("     -> Tabela extraída com sucesso.")
        # Retorna o DataFrame criado.
        return df
        
    except Exception as e:
        # Se qualquer outro erro ocorrer, imprime o erro e retorna None
        print(f"   - ERRO ao ler o arquivo de tabela: {e}")
        return None

def extrair_texto(caminho_arquivo: str) -> list[str]:
    """
    Extrai o texto corrido de arquivos .pdf ou .docx, parágrafo por parágrafo
    """
    print(f"   - Tentando extrair TEXTO de '{os.path.basename(caminho_arquivo)}'...")
    
    _, extensao = os.path.splitext(caminho_arquivo)
    extensao = extensao.lower()
    lista_paragrafos = [] # Inicializa uma lista vazia para armazenar os parágrafos.

    try:
        if extensao == '.pdf':
            # Usa a biblioteca pdfplumber para abrir e ler o PDF.
            with pdfplumber.open(caminho_arquivo) as pdf:
                # Corre cada página do documento.
                for pagina in pdf.pages:
                    texto_pagina = pagina.extract_text()
                    # Se algum texto for extraído da página
                    if texto_pagina:
                        # divide o texto da página por quebras de linha ('\n') para simular parágrafos
                        paragrafos_pagina = texto_pagina.split('\n')
                        # Adiciona os "parágrafos" encontrados à lista principal
                        lista_paragrafos.extend(paragrafos_pagina)

        elif extensao == '.docx':
            # Usa a biblioteca python-docx para abrir o documento Word
            documento = Document(caminho_arquivo)
            # A biblioteca já fornece uma lista de parágrafos
            for paragrafo in documento.paragraphs:
                # Adiciona o texto de cada parágrafo à lista
                lista_paragrafos.append(paragrafo.text)
        
        else:
            # Se a extensão não for suportada para textos, informa e retorna None
            print(f"   - ERRO: Extensão '{extensao}' não é suportada para extração de texto.")
            return None

        # Limpa a lista, removendo itens vazios ou que contêm apenas espaços
        paragrafos_filtrados = [] # Cria uma lista vazia para o resultado
        for p in lista_paragrafos: # Corre cada parágrafo extraído
            # A condição 'if p' verifica se a string não é vazia.
            # A condição 'not p.isspace()' verifica se a string não contém apenas espaços em branco
            if p and not p.isspace():
                # Remove espaços em branco do início e do fim do parágrafo
                paragrafos_filtrados.append(p.strip())

        
        # Se a lista final de parágrafos não estiver vazia
        if paragrafos_filtrados:
            print(f"     -> Texto extraído com sucesso. {len(paragrafos_filtrados)} parágrafos encontrados.")
            # Retorna a lista de parágrafos limpos.
            return paragrafos_filtrados
        else:
            # Se, após a filtragem, a lista estiver vazia, informa e retorna None
            print("   - AVISO: Nenhum texto foi encontrado no arquivo.")
            return None

    except Exception as e:
        # Se qualquer erro ocorrer durante o processo, imprime a mensagem e retorna None.
        print(f"   - ERRO ao extrair texto do arquivo: {e}")
        return None