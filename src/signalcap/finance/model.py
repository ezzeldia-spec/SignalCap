"""Pure, deterministic SaaS financial calculations."""

from signalcap.schemas import ExtractedSignals, MonthlyProjection


class SaaSFinancialModel:
    """Calculate projections from validated signals without external dependencies."""

    ZERO_CHURN_LTV_MONTH_CAP = 60

    def __init__(self, signals: ExtractedSignals) -> None:
        self.signals = signals

    def project_12_months(self) -> list[MonthlyProjection]:
        """Forecast MRR with churn applied before each month's acquisitions."""
        active_customers = 0.0
        new_customers = self.signals.monthly_leads * self.signals.expected_conversion_rate
        projection: list[MonthlyProjection] = []
        for month in range(1, 13):
            active_customers = active_customers * (1 - self.signals.monthly_churn_percentage) + new_customers
            projection.append(MonthlyProjection(
                month=month,
                active_customers=active_customers,
                mrr=active_customers * self.signals.willingness_to_pay,
            ))
        return projection

    def cac_payback_period_months(self) -> float | None:
        """Return ARPU months to recover CAC; undefined for zero ARPU."""
        if self.signals.willingness_to_pay == 0:
            return None
        return self.signals.estimated_cac / self.signals.willingness_to_pay

    def lifetime_value(self) -> float:
        """Return ARPU/churn, using a 60-month cap when churn is zero."""
        if self.signals.monthly_churn_percentage == 0:
            return self.signals.willingness_to_pay * self.ZERO_CHURN_LTV_MONTH_CAP
        return self.signals.willingness_to_pay / self.signals.monthly_churn_percentage
