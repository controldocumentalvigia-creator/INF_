from __future__ import annotations
import html
import pandas as pd
import streamlit as st
from config import ROYAL_BLUE, TEXT_DARK
from utils import fmt_cop, fmt_int, fmt_pct

def inject_css() -> None:
    st.markdown(f"""<style>.stApp{{background:#F4F7FB;color:{TEXT_DARK};}}.block-container{{padding-top:1rem;max-width:1700px;}}h1,h2,h3,h4,p,span,label,div{{color:{TEXT_DARK};}}[data-testid='stSidebar']{{background:linear-gradient(180deg,#003B8E,#082F49);}}[data-testid='stSidebar'] *{{color:white!important;}}.kpi{{background:white;border-radius:14px;padding:14px 16px;border-left:5px solid {ROYAL_BLUE};box-shadow:0 4px 14px rgba(15,23,42,.10);min-height:105px;}}.kpi-title{{font-size:.76rem;font-weight:800;color:#1F2937;text-transform:uppercase;}}.kpi-value{{font-size:1.55rem;font-weight:900;color:#111827;margin-top:8px;}}.kpi-note{{font-size:.78rem;font-weight:650;color:#374151;margin-top:6px;}}thead th{{background:{ROYAL_BLUE}!important;color:white!important;font-weight:800!important;text-align:center!important;}}tbody td{{color:#111827!important;font-weight:600;}}</style>""",unsafe_allow_html=True)

def kpi_card(title: str,value: str,note: str="") -> None:
    st.markdown(f"<div class='kpi'><div class='kpi-title'>{html.escape(title)}</div><div class='kpi-value'>{html.escape(value)}</div><div class='kpi-note'>{html.escape(note)}</div></div>",unsafe_allow_html=True)

def show_kpis(k: dict) -> None:
    r1=st.columns(4)
    with r1[0]: kpi_card("Total servicios válidos",fmt_int(k["servicios"]),"Sin anulados")
    with r1[1]: kpi_card("Facturación",fmt_cop(k["facturacion"]),"V.CLIENTE")
    with r1[2]: kpi_card("Margen",fmt_cop(k["margen"]),"V.CLIENTE - V.CONDUCT")
    with r1[3]: kpi_card("Rentabilidad",fmt_pct(k["rentabilidad"]),"Margen / Facturación")
    r2=st.columns(4)
    with r2[0]: kpi_card("OTIF operativo",fmt_pct(k["otif"]),"CUMPLIDO / Total válido")
    with r2[1]: kpi_card("Cumplimiento de cierre",fmt_pct(k["cumplimiento_cierre"]),"CUMPLIDO OPERATIVO / Total válido")
    with r2[2]: kpi_card("Pendientes operativos (%)",fmt_pct(k["pendientes_pct"]),"No incluye CUMPLIDO ni CUMPLIDO OPERATIVO")
    with r2[3]: kpi_card("Pendientes operativos",fmt_int(k["pendientes"]),"Cantidad pendiente")

def styled_table(df: pd.DataFrame,height: int=420) -> None:
    st.dataframe(df,use_container_width=True,height=height,hide_index=True)
