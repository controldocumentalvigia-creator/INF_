from __future__ import annotations
import re, unicodedata
from typing import Iterable, Optional
import pandas as pd

def normalize_text(value: object) -> str:
    if value is None: return ""
    text = str(value).strip().upper()
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", text)

def normalize_col(value: object) -> str:
    text = normalize_text(value).replace("_", " ").replace("-", " ")
    text = re.sub(r"[^A-Z0-9 ]", "", text)
    return re.sub(r"\s+", " ", text).strip()

def find_column(df: pd.DataFrame, candidates: Iterable[str]) -> Optional[str]:
    normalized = {normalize_col(c): c for c in df.columns}
    for candidate in candidates:
        key = normalize_col(candidate)
        if key in normalized: return normalized[key]
    return None

def to_money(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_numeric(series, errors="coerce").fillna(0.0)
    cleaned = (series.astype(str).str.replace(r"[^0-9,\.\-]", "", regex=True)
               .str.replace(".", "", regex=False).str.replace(",", ".", regex=False))
    return pd.to_numeric(cleaned, errors="coerce").fillna(0.0)

def fmt_cop(value: float) -> str:
    try: return "$ " + f"{float(value):,.0f}".replace(",", ".")
    except Exception: return "$ 0"

def fmt_pct(value: float) -> str:
    try: return f"{float(value)*100:,.2f} %".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception: return "0,00 %"

def fmt_int(value: float) -> str:
    try: return f"{int(round(float(value))):,}".replace(",", ".")
    except Exception: return "0"
