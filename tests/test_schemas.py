import pytest
from pydantic import ValidationError

from signalcap.schemas import ExtractedSignals, ProjectionResponse


def test_extracted_signals_accepts_valid_values() -> None:
    signals = ExtractedSignals(
        willingness_to_pay=100.0, estimated_cac=300.0,
        monthly_churn_percentage=0.05, expected_conversion_rate=0.1, monthly_leads=40,
    )
    assert signals.monthly_leads == 40


def test_projection_response_has_exact_twelve_month_contract() -> None:
    signals = ExtractedSignals(
        willingness_to_pay=100.0, estimated_cac=300.0,
        monthly_churn_percentage=0.05, expected_conversion_rate=0.1, monthly_leads=40,
    )
    response = ProjectionResponse(
        monthly_mrr=[0.0] * 12,
        cac_payback_period_months=3.0,
        ltv=2000.0,
        extracted_signals=signals,
    )
    assert len(response.monthly_mrr) == 12


@pytest.mark.parametrize("field,value", [
    ("monthly_churn_percentage", 1.01), ("expected_conversion_rate", -0.01),
    ("monthly_leads", -1), ("willingness_to_pay", -1.0), ("estimated_cac", -1.0),
])
def test_extracted_signals_rejects_values_outside_contract(field: str, value: float | int) -> None:
    data = dict(willingness_to_pay=100.0, estimated_cac=300.0, monthly_churn_percentage=0.05,
                expected_conversion_rate=0.1, monthly_leads=40)
    data[field] = value
    with pytest.raises(ValidationError):
        ExtractedSignals(**data)
