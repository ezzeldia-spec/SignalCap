import pytest
from pydantic import ValidationError

from signalcap.schemas import ExtractedSignals


def test_extracted_signals_accepts_valid_contract() -> None:
    signals = ExtractedSignals(
        willingness_to_pay=100.0,
        estimated_cac=250.0,
        monthly_churn_percentage=0.05,
        expected_conversion_rate=0.1,
        monthly_leads=50,
    )

    assert signals.monthly_leads == 50


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("monthly_churn_percentage", 1.01),
        ("expected_conversion_rate", -0.01),
        ("monthly_leads", -1),
        ("willingness_to_pay", -1.0),
        ("estimated_cac", -1.0),
    ],
)
def test_extracted_signals_rejects_invalid_values(field: str, value: float | int) -> None:
    values = {
        "willingness_to_pay": 100.0,
        "estimated_cac": 250.0,
        "monthly_churn_percentage": 0.05,
        "expected_conversion_rate": 0.1,
        "monthly_leads": 50,
    }
    values[field] = value

    with pytest.raises(ValidationError):
        ExtractedSignals(**values)
