from pathlib import Path
import pandas as pd
from rdgp.evidence import build_evidence_item, validate_evidence_item

def test_example_evidence_items_validate():
    path=Path("data/example/evidence_items.tsv")
    df=pd.read_csv(path,sep="\t",dtype=str,keep_default_na=False)

    for _,row in df.iterrows():
        item=build_evidence_item(row.to_dict())
        assert validate_evidence_item(item)==[]

def test_example_evidence_items_preserve_direction_and_context():
    path=Path("data/example/evidence_items.tsv")
    df=pd.read_csv(path,sep="\t",dtype=str,keep_default_na=False)

    directions=set(df["evidence_direction"])
    categories=set(df["evidence_category"])

    assert "supportive" in directions
    assert "context_modifying" in directions
    assert "uncertainty_preserving" in directions
    assert "variant" in categories
    assert "inheritance" in categories
    assert "mechanistic" in categories

def test_example_evidence_items_do_not_require_score_or_probability():
    path=Path("data/example/evidence_items.tsv")
    df=pd.read_csv(path,sep="\t",dtype=str,keep_default_na=False)

    assert "priority_score" not in df.columns
    assert "posterior_probability" not in df.columns
