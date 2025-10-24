import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da pagina
st.set_page_config(page_title='MC SONAE', layout='wide')

# Lendo df
df = pd.read_csv("saida/empresas_2_tratado.csv")

# Titulo
st.title("Análise de Empresas - MC SONAE")

# Função para formatação de dinheiro 
fmt_moeda = lambda x: f"R$ {x:,.2f}"
fmt_num = lambda x: f"{x:,}"

# KPIs
st.subheader("Visão Geral")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Receita Total", fmt_moeda(df['Receita Total (receita bruta)'].sum()))
col2.metric("Lucro Líquido", fmt_moeda(df['Lucro Líquido'].sum()))
col3.metric("Custo (OPEX)", fmt_moeda(df['Custo Operacional (OPEX)'].sum()))
col4.metric("Funcionários", fmt_num(df['Número de Funcionários'].sum()))
st.divider()

# Graficos
col1, col2 = st.columns(2)

# Receita por Ano
with col1:
    fig = px.bar(
        df.groupby('Ano', as_index=False)['Receita Total (receita bruta)'].sum(),
        x='Ano', y='Receita Total (receita bruta)',
        title='Receita Total por Ano'
    )
    st.plotly_chart(fig, use_container_width=True)

# Receita por Setor
with col2:
    fig = px.bar(
        df.groupby('Setor', as_index=False)['Receita Total (receita bruta)'].sum(),
        x='Setor', y='Receita Total (receita bruta)',
        title='Receita Total por Setor'
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()
col1, col2 = st.columns(2)

# Top 5 Empresas
with col1:
    top5 = (df.groupby('Empresa')['Receita Total (receita bruta)']
            .sum().nlargest(5).reset_index())
    fig = px.bar(top5, y='Empresa', x='Receita Total (receita bruta)',
                 orientation='h', title='Top 5 Empresas por Receita')
    st.plotly_chart(fig, use_container_width=True)

# Lucro por País
with col2:
    fig = px.bar(
        df.groupby('País', as_index=False)['Lucro Líquido'].sum(),
        x='País', y='Lucro Líquido',
        title='Lucro Líquido por País'
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Checkbox pra mostrar df
if st.checkbox("Mostrar Dados Filtrados"):
    st.dataframe(df)
