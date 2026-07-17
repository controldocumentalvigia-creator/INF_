from __future__ import annotations
import pandas as pd
import streamlit as st

def _multi(df: pd.DataFrame,label: str,col: str,key: str) -> pd.DataFrame:
    options = sorted(df[col].dropna().astype(str).unique().tolist())
    selected = st.multiselect(label,options,default=[],key=key)
    return df[df[col].astype(str).isin(selected)].copy() if selected else df

def sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.markdown("## Filtros")
    years = sorted([int(x) for x in df["__ANIO__"].dropna().unique()])
    sy = st.sidebar.multiselect("Año",years,default=[],key="flt_year")
    if sy: df = df[df["__ANIO__"].isin(sy)].copy()
    months = sorted(df["__MES__"].dropna().unique().tolist())
    sm = st.sidebar.multiselect("Mes",months,default=[],key="flt_month")
    if sm: df = df[df["__MES__"].isin(sm)].copy()
    for label,col,key in [("Cliente","__CLIENTE__","flt_client"),("Quién creó","__QUIEN_CREO__","flt_creator"),("Estado OP","__ESTADO_OP__","flt_state"),("Línea de negocio","__LINEA_NEGOCIO__","flt_line"),("Tipo de negocio","__TIPO_NEGOCIO__","flt_type"),("Placa","__PLACA__","flt_plate"),("Conductor","__CONDUCTOR__","flt_driver")]:
        df = _multi(df,label,col,key)
    st.sidebar.caption(f"Registros filtrados: {len(df):,}".replace(",","."))
    return df
