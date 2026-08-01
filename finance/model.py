"""Pure deterministic SaaS financial model interface."""

from signalcap.schemas import ExtractedSignals, MonthlyProjection


class SaaSFinancialModel:
    """Financial engine that consumes validated signals only.

    This class must never call an LLM or depend on the extraction layer.
    """

    def __init__(self, signals: ExtractedSignals) -> None:
        self.signals = signals

    def project_12_months(self) -> list[MonthlyProjection]:
        """Return twelve months of active-customer and MRR projections."""
        raise NotImplementedError("Financial projection logic has not been implemented yet")

    def cac_payback_period_months(self) -> float | None:
        """Return CAC payback in months."""
        raise NotImplementedError("CAC payback logic has not been implemented yet")

    def lifetime_value(self) -> float:
        """Return LTV using the bounded zero-churn rule."""
        raise NotImplementedError("LTV logic has not been implemented yet")
