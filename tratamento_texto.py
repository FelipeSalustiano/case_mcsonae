"""
Módulo de Tratamento de Texto

Este módulo contém funções para processamento e análise de texto.
As operações incluem limpeza (remoção de pontuação, normalização de caixa)
e a geração de estatísticas básicas, como contagem de palavras.
"""

import re
from collections import Counter
import string 

def limpar_texto(texto: str) -> str:
    """
    Realiza uma limpeza básica no texto.
    """
    # Etapa 1: Converte toda a string para letras minúsculas
    texto = texto.lower()
    
    # Etapa 2: Remove todos os caracteres de pontuação.
    # 'string.punctuation' é uma string que contém todos os sinais de pontuação comuns.
    # O método 'translate' é uma forma eficiente de remover múltiplos caracteres de uma vez.
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    
    # Etapa 3: Normaliza os espaços em branco.
    # 'texto.split()' quebra a string em uma lista de palavras (removendo espaços extras)
    # "' '.join(...)" junta a lista de volta em uma string, com um único espaço entre as palavras
    texto = ' '.join(texto.split())
    
    return texto

def gerar_estatisticas_texto(texto_limpo: str) -> dict:
    """
    Gera um dicionário com estatísticas básicas sobre o texto
    """
    # Quebra a string de texto em uma lista de palavras
    palavras = texto_limpo.split()
    
    # Calcula o número total de palavras na lista
    total_palavras = len(palavras)
    
    # 'set(palavras)' cria um conjunto, que automaticamente remove duplicatas.
    # 'len()' então nos dá o número de palavras únicas.
    palavras_unicas = len(set(palavras))
    
    # 'Counter' é uma classe especializada que conta a frequência de cada item em uma lista
    frequencia_palavras = Counter(palavras)
    # '.most_common(5)' retorna uma lista de tuplas com as 5 palavras mais frequentes e suas contagens
    top_5_palavras = frequencia_palavras.most_common(5)
    
    # Monta o dicionário final com os resultados
    estatisticas = {
        "total_de_palavras": total_palavras,
        "total_de_palavras_unicas": palavras_unicas,
        "top_5_palavras_mais_comuns": top_5_palavras
    }
    
    return estatisticas