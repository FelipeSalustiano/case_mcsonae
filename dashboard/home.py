import streamlit as st
import pandas as pd

# Lendo df
df = pd.read_csv('saida\empresas_2_tratado.csv')

# Informações sobre a base de dados
total_empresas = len(df['Empresa'].unique())
setores = len(df['Setor'].unique())
funcionarios = df['Número de Funcionários'].sum()

# Configuração da página
st.set_page_config(
    page_title="MC SONAE - Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- Cabeçalho ---
st.title("📊 DASHBOARD - MC SONAE")
st.markdown("<h4 style='color:#6c63ff;'>Bem-vindo à análise de empresas da MC SONAE!</h4>", unsafe_allow_html=True)
st.markdown("---")

# --- Texto de introdução ---
st.write("""
Este painel foi desenvolvido para **explorar e visualizar dados das empresas participantes** do MC SONAE.  
Aqui você pode navegar entre diferentes páginas para visualizar indicadores, gráficos e conclusões sobre o desempenho das empresas.
""")

# --- Métricas principais ---
col1, col2, col3 = st.columns(3)
col1.metric("🏢 Total de Empresas", total_empresas, "+1")
col2.metric("💼 Setores Ativos", setores, "-3")
col3.metric("📈 Total Funcionários", funcionarios, "+2%")

# --- Divisor visual ---
st.markdown("---")

# --- Rodapé discreto ---
st.markdown(
    "<p style='text-align:center; color:gray;'>Use o menu lateral para acessar as demais páginas do dashboard!</p>",
    unsafe_allow_html=True
)
