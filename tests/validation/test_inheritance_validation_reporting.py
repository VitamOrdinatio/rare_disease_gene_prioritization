from rdgp.inheritance import evaluate_inheritance_context
from rdgp.validators import (
    validation_result_to_dict,
    summarize_validation_results,
    ValidationResult,
)

def test_inheritance_validation_summary_remains_visible():
    inheritance=evaluate_inheritance_context(
        "autosomal_recessive",
        "heterozygous",
    )

    result=ValidationResult(
        passed=True,
        errors=[],
        warnings=[
            inheritance["inheritance_explanation"]
        ],
    )

    summary=summarize_validation_results([
        validation_result_to_dict(result,"inheritance_validation")
    ])

    assert summary["warning_count"] >= 1

def test_inheritance_validation_not_collapsed_into_generic_validation():
    inheritance=evaluate_inheritance_context(
        "unknown",
        "unknown",
    )

    result=ValidationResult(
        passed=True,
        errors=[],
        warnings=[
            inheritance["inheritance_explanation"]
        ],
    )

    summary=summarize_validation_results([
        validation_result_to_dict(result,"inheritance_validation")
    ])

    labels=[
        item["label"]
        for item in summary["results"]
    ]

    assert "inheritance_validation" in labels
