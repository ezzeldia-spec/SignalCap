import pytest

from signalcap.finance import SaaSFinancialModel
from signalcap.schemas import ExtractedSignals


def make_signals(**overrides: float | int) -> ExtractedSignals:
    values: dict[str, float | int] = dict(
        willingness_to_pay=100.0, estimated_cac=300.0, monthly_churn_percentage=0.1,
        expected_conversion_rate=0.1, monthly_leads=100,
    )
    values.update(overrides)
    return ExtractedSignals(**values)


def test_projection_applies_churn_before_monthly_acquisitions() -> None:
    response = SaaSFinancialModel(make_signals()).generate_projection()
    assert len(response.monthly_mrr) == 12
    assert response.monthly_mrr[0] == 1000
    assert response.monthly_mrr[1] == 1900
    assert response.monthly_mrr[-1] == pytest.approx(7175.70463519)
    assert response.extracted_signals.monthly_leads == 100


def test_cac_payback_and_ltv_are_deterministic() -> None:
    model = SaaSFinancialModel(make_signals())
    response = model.generate_projection()
    assert response.cac_payback_period_months == 3
    assert response.ltv == 1000


def test_zero_churn_uses_sixty_month_ltv_cap() -> None:
    model = SaaSFinancialModel(make_signals(monthly_churn_percentage=0))
    response = model.generate_projection()
    assert response.ltv == 6000
    assert response.monthly_mrr[-1] == 12000


@pytest.mark.parametrize("overrides", [{"expected_conversion_rate": 0}, {"monthly_leads": 0}])
def test_zero_acquisition_inputs_produce_zero_projection(overrides: dict[str, float | int]) -> None:
    response = SaaSFinancialModel(make_signals(**overrides)).generate_projection()
    assert response.monthly_mrr == [0.0] * 12


def test_zero_arpu_does_not_divide_by_zero_for_payback() -> None:
    model = SaaSFinancialModel(make_signals(willingness_to_pay=0))
    response = model.generate_projection()
    assert response.cac_payback_period_months is None
    assert response.monthly_mrr == [0.0] * 12
    assert response.ltv == 0
