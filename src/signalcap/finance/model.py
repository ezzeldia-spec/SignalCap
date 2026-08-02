"""Pure, deterministic SaaS financial calculations."""

from signalcap.schemas import ExtractedSignals, ProjectionResponse


ZERO_CHURN_LTV_MONTH_CAP = 60
"""Maximum lifetime used when zero churn would otherwise divide by zero."""


class SaaSFinancialModel:
    """Calculate projections from validated signals without external dependencies."""

    def __init__(self, signals: ExtractedSignals) -> None:
        self.signals = signals

    def project_12_months(self) -> list[float]:
        """Forecast MRR with churn applied before each month's acquisitions."""
        active_customers = 0.0
        new_customers = self.signals.monthly_leads * self.signals.expected_conversion_rate
        monthly_mrr: list[float] = []
        for month in range(1, 13):
            active_customers = active_customers * (1 - self.signals.monthly_churn_percentage) + new_customers
            monthly_mrr.append(active_customers * self.signals.willingness_to_pay)
        return monthly_mrr

    def cac_payback_period_months(self) -> float | None:
        """Return ARPU months to recover CAC; undefined for zero ARPU."""
        if self.signals.willingness_to_pay == 0:
            return None
        return self.signals.estimated_cac / self.signals.willingness_to_pay

    def lifetime_value(self) -> float:
        """Return ARPU/churn, using a 60-month cap when churn is zero."""
        if self.signals.monthly_churn_percentage == 0:
            return self.signals.willingness_to_pay * ZERO_CHURN_LTV_MONTH_CAP
        return self.signals.willingness_to_pay / self.signals.monthly_churn_percentage

    def generate_projection(self) -> ProjectionResponse:
        """Return the complete deterministic model output for the validated signals."""
        return ProjectionResponse(
            monthly_mrr=self.project_12_months(),
            cac_payback_period_months=self.cac_payback_period_months(),
            ltv=self.lifetime_value(),
            extracted_signals=self.signals,
        )
