from __future__ import annotations
import numpy as np
import pandas as pd

def safe_div(num: float, den: float) -> float:
    return float(num)/float(den) if den else 0.0

def general_kpis(df: pd.DataFrame) -> dict:
    total = len(df); fact = float(df["__V_CLIENTE__"].sum()); cost = float(df["__V_CONDUCT__"].sum()); margin = fact-cost
    cumplido = int((df["__ESTADO_OP__"]=="CUMPLIDO").sum())
    cumplido_op = int((df["__ESTADO_OP__"]=="CUMPLIDO OPERATIVO").sum())
    en_programacion = int((df["__ESTADO_OP__"]=="EN PROGRAMACION").sum())
    en_transito = int((df["__ESTADO_OP__"]=="EN TRANSITO").sum())
    pendientes = int((~df["__ESTADO_OP__"].isin(["CUMPLIDO","CUMPLIDO OPERATIVO"])).sum())
    return {"servicios":total,"facturacion":fact,"costos":cost,"margen":margin,"rentabilidad":safe_div(margin,fact),"otif":safe_div(cumplido,total),"cumplimiento_cierre":safe_div(cumplido_op,total),"pendientes_pct":safe_div(pendientes,total),"pendientes":pendientes,"cumplido":cumplido,"cumplido_operativo":cumplido_op,"en_programacion":en_programacion,"en_transito":en_transito}

def by_client(df: pd.DataFrame) -> pd.DataFrame:
    out = df.groupby("__CLIENTE__",as_index=False).agg(Servicios=("__SERVICIOS__","sum"),Facturacion=("__V_CLIENTE__","sum"),Costos=("__V_CONDUCT__","sum"),Margen=("__MARGEN__","sum"))
    out["Rentabilidad"] = np.where(out["Facturacion"].ne(0),out["Margen"]/out["Facturacion"],0.0)
    return out.sort_values("Facturacion",ascending=False)

def state_matrix(df: pd.DataFrame, row) -> pd.DataFrame:
    pivot = pd.pivot_table(df,index=row,columns="__ESTADO_OP__",values="__SERVICIOS__",aggfunc="sum",fill_value=0)
    pivot["TOTAL GENERAL"] = pivot.sum(axis=1)
    return pivot.sort_values("TOTAL GENERAL",ascending=False).reset_index()
