from __future__ import annotations
import io
from typing import Dict, Optional, Tuple
import pandas as pd
import streamlit as st
from config import COLUMN_CANDIDATES, MONTHS_ES
from utils import find_column, normalize_text, to_money

@st.cache_data(show_spinner=False)
def get_excel_sheets(file_bytes: bytes, filename: str) -> list[str]:
    engine = "xlrd" if filename.lower().endswith(".xls") else "openpyxl"
    return pd.ExcelFile(io.BytesIO(file_bytes), engine=engine).sheet_names

@st.cache_data(show_spinner=False)
def load_file(file_bytes: bytes, filename: str, sheet_name: Optional[str]) -> pd.DataFrame:
    name = filename.lower()
    if name.endswith(".csv"):
        try: df = pd.read_csv(io.BytesIO(file_bytes), sep=None, engine="python", encoding="utf-8")
        except UnicodeDecodeError: df = pd.read_csv(io.BytesIO(file_bytes), sep=None, engine="python", encoding="latin1")
    elif name.endswith(".xls"):
        df = pd.read_excel(io.BytesIO(file_bytes), sheet_name=sheet_name, engine="xlrd")
    else:
        df = pd.read_excel(io.BytesIO(file_bytes), sheet_name=sheet_name, engine="openpyxl")
    df.columns = [str(c).strip() for c in df.columns]
    return df.dropna(how="all").copy()

@st.cache_data(show_spinner=False)
def prepare_data(raw: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Optional[str]]]:
    df = raw.copy()
    colmap = {k: find_column(df, v) for k, v in COLUMN_CANDIDATES.items()}
    fecha_col = colmap["fecha"]
    df["__FECHA__"] = pd.to_datetime(df[fecha_col], errors="coerce", dayfirst=True) if fecha_col else pd.NaT
    df["__ANIO__"] = df["__FECHA__"].dt.year.astype("Int64")
    df["__MES_NUM__"] = df["__FECHA__"].dt.month.astype("Int64")
    df["__MES__"] = df["__MES_NUM__"].map(MONTHS_ES)
    df["__PERIODO__"] = df["__FECHA__"].dt.to_period("M").astype(str)
    vc, vd = colmap["valor_cliente"], colmap["valor_conductor"]
    df["__V_CLIENTE__"] = to_money(df[vc]) if vc else 0.0
    df["__V_CONDUCT__"] = to_money(df[vd]) if vd else 0.0
    df["__MARGEN__"] = df["__V_CLIENTE__"] - df["__V_CONDUCT__"]
    df["__SERVICIOS__"] = 1
    estado_col = colmap["estado_op"]
    df["__ESTADO_OP__"] = df[estado_col].fillna("SIN DATO").map(normalize_text) if estado_col else "SIN DATO"
    df = df.loc[df["__ESTADO_OP__"] != "ANULADO"].copy()
    mapping = {"cliente":"__CLIENTE__","quien_creo":"__QUIEN_CREO__","placa":"__PLACA__","origen":"__ORIGEN__","destino":"__DESTINO__","linea_negocio":"__LINEA_NEGOCIO__","tipo_negocio":"__TIPO_NEGOCIO__","tipo_vehiculo":"__TIPO_VEHICULO__"}
    for logical, output in mapping.items():
        source = colmap.get(logical)
        df[output] = df[source].fillna("SIN DATO").astype(str).str.strip() if source else "SIN DATO"
    if raw.shape[1] >= 23:
        source_w = raw.columns[22]
        df["__CONDUCTOR__"] = raw.loc[df.index, source_w].fillna("SIN DATO").astype(str).str.strip()
        colmap["conductor"] = source_w
    else:
        df["__CONDUCTOR__"] = "SIN DATO"; colmap["conductor"] = None
    return df, colmap
