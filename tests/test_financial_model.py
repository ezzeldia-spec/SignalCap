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
    projection = SaaSFinancialModel(make_signals()).project_12_months()
    assert len(projection) == 12
    assert projection[0].active_customers == 10
    assert projection[1].active_customers == 19
    assert projection[1].mrr == 1900
    assert projection[-1].active_customers == pytest.approx(71.7570463519)


def test_cac_payback_and_ltv_are_deterministic() -> None:
    model = SaaSFinancialModel(make_signals())
    assert model.cac_payback_period_months() == 3
    assert model.lifetime_value() == 1000


def test_zero_churn_uses_sixty_month_ltv_cap() -> None:
    model = SaaSFinancialModel(make_signals(monthly_churn_percentage=0))
    assert model.lifetime_value() == 6000
    assert model.project_12_months()[-1].active_customers == 120


@pytest.mark.parametrize("overrides", [{"expected_conversion_rate": 0}, {"monthly_leads": 0}])
def test_zero_acquisition_inputs_produce_zero_projection(overrides: dict[str, float | int]) -> None:
    projection = SaaSFinancialModel(make_signals(**overrides)).project_12_months()
    assert all(month.active_customers == 0 and month.mrr == 0 for month in projection)


def test_zero_arpu_does_not_divide_by_zero_for_payback() -> None:
    model = SaaSFinancialModel(make_signals(willingness_to_pay=0))
    assert model.cac_payback_period_months() is None
    assert model.lifetime_value() == 0
