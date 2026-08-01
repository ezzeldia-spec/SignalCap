"""Pydantic contracts shared across SignalCap layers."""

from pydantic import BaseModel, ConfigDict, Field, field_validator


class InterviewTranscript(BaseModel):
    """Raw qualitative interview material submitted for extraction."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    transcript: str = Field(min_length=1)


class ExtractedSignals(BaseModel):
    """Validated commercial inputs produced by the extraction boundary."""

    model_config = ConfigDict(extra="forbid")

    willingness_to_pay: float = Field(ge=0, description="Monthly ARPU in USD.")
    estimated_cac: float = Field(ge=0, description="Customer acquisition cost in USD.")
    monthly_churn_percentage: float = Field(
        ge=0, le=1, description="Monthly churn as a decimal fraction."
    )
    expected_conversion_rate: float = Field(
        ge=0, le=1, description="Lead-to-customer conversion as a decimal fraction."
    )
    monthly_leads: int = Field(ge=0, description="New monthly leads entering the funnel.")

    @field_validator("monthly_churn_percentage", "expected_conversion_rate")
    @classmethod
    def validate_fraction(cls, value: float) -> float:
        """Preserve the explicit fraction contract at the schema boundary."""
        if not 0 <= value <= 1:
            raise ValueError("must be between 0 and 1")
        return value

    @field_validator("willingness_to_pay", "estimated_cac", "monthly_leads")
    @classmethod
    def validate_non_negative(cls, value: float | int) -> float | int:
        """Preserve the non-negative commercial-input contract."""
        if value < 0:
            raise ValueError("must be non-negative")
        return value


class MonthlyProjection(BaseModel):
    """One month of deterministic model output (implementation pending)."""

    month: int = Field(ge=1, le=12)
    active_customers: float = Field(ge=0)
    mrr: float = Field(ge=0)


class ProjectionResponse(BaseModel):
    """Strict API response contract for a generated financial model."""

    signals: ExtractedSignals
    monthly_projection: list[MonthlyProjection] = Field(min_length=12, max_length=12)
    cac_payback_period_months: float | None = Field(default=None, ge=0)
    lifetime_value: float = Field(ge=0)
