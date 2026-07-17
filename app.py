# -*- coding: utf-8 -*-
from __future__ import annotations
import streamlit as st
from components import inject_css, show_kpis, styled_table
from data import get_excel_sheets, load_file, prepare_data
from filters import sidebar_filters
from kpis import by_client, general_kpis, state_matrix

st.set_page_config(page_title="VIGÍA INSIGHT",page_icon="📊",layout="wide",initial_sidebar_state="expanded")
inject_css()
st.title("📊 VIGÍA INSIGHT")
st.caption("Centro de Control Gerencial Operativo y Financiero")
st.sidebar.markdown("## Cargar base principal")
uploaded = st.sidebar.file_uploader("Excel o CSV",type=["xlsx","xls","xlsm","csv"])
if uploaded is None:
    st.info("Carga la base principal desde la barra lateral para iniciar.")
    st.stop()
file_bytes = uploaded.getvalue(); sheet = None
if not uploaded.name.lower().endswith(".csv"):
    sheets = get_excel_sheets(file_bytes,uploaded.name)
    sheet = st.sidebar.selectbox("Hoja a analizar",sheets)
with st.spinner("Preparando información..."):
    raw = load_file(file_bytes,uploaded.name,sheet)
    prepared,colmap = prepare_data(raw)
df = sidebar_filters(prepared)
if df.empty:
    st.warning("No hay registros con los filtros seleccionados.")
    st.stop()
show_kpis(general_kpis(df))
tab1,tab2,tab3 = st.tabs(["Resumen","Clientes","Cierre operativo"])
with tab1:
    st.subheader("Resumen por cliente")
    styled_table(by_client(df))
with tab2:
    st.subheader("Cliente vs Estado OP")
    styled_table(state_matrix(df,"__CLIENTE__"))
with tab3:
    c1,c2 = st.columns(2)
    with c1:
        st.subheader("Quién creó vs Estado OP")
        styled_table(state_matrix(df,"__QUIEN_CREO__"))
    with c2:
        st.subheader("Cliente + Quién creó vs Estado OP")
        styled_table(state_matrix(df,["__CLIENTE__","__QUIEN_CREO__"]))
