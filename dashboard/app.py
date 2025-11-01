import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="MC SONAE - Análise de Empresas",
    layout="wide"
)

# Lendo df
df = pd.read_csv("saida/empresas_2_tratado.csv")

# Título
st.title("Análise de Empresas - MC SONAE")

# Filtros
st.sidebar.header("🔎 Filtros")

empresa = st.sidebar.selectbox("Selecione a empresa", ["Todas"] + sorted(df["Empresa"].unique()))
ano = st.sidebar.multiselect("Selecione o(s) ano(s)", sorted(df["Ano"].unique()))
setor = st.sidebar.multiselect("Selecione o(s) setor(es)", sorted(df["Setor"].unique()))
pais = st.sidebar.multiselect("Selecione o(s) país(es)", sorted(df["País"].unique()))

df_filtrado = df.copy()

if empresa != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Empresa"] == empresa]

if ano:
    df_filtrado = df_filtrado[df_filtrado["Ano"].isin(ano)]

if setor:
    df_filtrado = df_filtrado[df_filtrado["Setor"].isin(setor)]

if pais:
    df_filtrado = df_filtrado[df_filtrado["País"].isin(pais)]

# Funções de formatação
fmt_moeda = lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
fmt_num = lambda x: f"{x:,}".replace(",", ".")


# KPIs
st.subheader("Visão Geral")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Receita Total", fmt_moeda(df_filtrado["Receita Total (receita bruta)"].sum()))
col2.metric("Lucro Líquido", fmt_moeda(df_filtrado["Lucro Líquido"].sum()))
col3.metric("Custo Operacional (OPEX)", fmt_moeda(df_filtrado["Custo Operacional (OPEX)"].sum()))
col4.metric("Total de Funcionários", fmt_num(df_filtrado["Número de Funcionários"].sum()))

st.divider()

# Gráficos 
col1, col2 = st.columns(2)

with col1:
    receita_ano = df_filtrado.groupby("Ano", as_index=False)["Receita Total (receita bruta)"].sum()
    fig = px.bar(
        receita_ano,
        x="Ano",
        y="Receita Total (receita bruta)",
        title="Receita Total por Ano",
        color="Ano",
        text_auto=".2s"
    )
    fig.update_layout(xaxis_title=None, yaxis_title="Receita (R$)", showlegend=False)
    fig.update_yaxes(showticklabels=False, showgrid=False, showline=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    receita_setor = df_filtrado.groupby("Setor", as_index=False)["Receita Total (receita bruta)"].sum()
    fig = px.bar(
        receita_setor,
        x="Setor",
        y="Receita Total (receita bruta)",
        title="Receita Total por Setor",
        color="Setor",
        text_auto=".2s"
    )
    fig.update_layout(xaxis_title=None, yaxis_title="Receita (R$)", showlegend=False)
    fig.update_yaxes(showticklabels=False, showgrid=False, showline=False)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

col1, col2 = st.columns(2)

with col1:
    top5 = (
        df.groupby("Empresa")["Receita Total (receita bruta)"]
        .sum()
        .nlargest(5)
        .reset_index()
    )
    fig = px.bar(
        top5,
        y="Empresa",
        x="Receita Total (receita bruta)",
        orientation="h",
        title="Top 5 Empresas por Receita",
        color="Empresa",
        text_auto=".2s"
    )
    fig.update_layout(xaxis_title="Receita (R$)", yaxis_title=None, showlegend=False)
    fig.update_yaxes(showticklabels=False, showgrid=False, showline=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    lucro_pais = df_filtrado.groupby("País", as_index=False)["Lucro Líquido"].sum()
    fig = px.bar(
        lucro_pais,
        x="País",
        y="Lucro Líquido",
        title="Lucro Líquido por País",
        color="País",
        text_auto=".2s"
    )
    fig.update_layout(xaxis_title=None, yaxis_title="Lucro (R$)", showlegend=False)
    fig.update_yaxes(showticklabels=False, showgrid=False, showline=False)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Mostrar tabela 
if st.checkbox("Mostrar Dados Filtrados"):
    st.dataframe(df_filtrado, use_container_width=True)
