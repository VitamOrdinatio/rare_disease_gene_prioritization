"""Input/output helpers for RDGP."""
from __future__ import annotations
from pathlib import Path
import pandas as pd

def read_tsv(path:str|Path)->pd.DataFrame:
    path=Path(path)
    if not path.exists():
        raise FileNotFoundError(f"TSV file not found: {path}")
    return pd.read_csv(path,sep="\t",dtype=str,keep_default_na=False)

def write_tsv(df:pd.DataFrame,path:str|Path)->Path:
    path=Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(path,sep="\t",index=False)
    return path
