"""Validated contracts shared across SignalCap layers."""

from pydantic import BaseModel, ConfigDict, Field, field_validator


class InterviewTranscript(BaseModel):
    """Raw qualitative interview material submitted for model generation."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    transcript: str = Field(min_length=1)


class ExtractedSignals(BaseModel):
    """Commercial inputs extracted by the probabilistic boundary."""

    model_config = ConfigDict(extra="forbid")
    willingness_to_pay: float = Field(ge=0, description="Monthly ARPU in USD.")
    estimated_cac: float = Field(ge=0, description="Customer acquisition cost in USD.")
    monthly_churn_percentage: float = Field(ge=0, le=1)
    expected_conversion_rate: float = Field(ge=0, le=1)
    monthly_leads: int = Field(ge=0)

    @field_validator("monthly_churn_percentage", "expected_conversion_rate")
    @classmethod
    def validate_fraction(cls, value: float) -> float:
        if not 0 <= value <= 1:
            raise ValueError("must be between 0 and 1")
        return value

    @field_validator("willingness_to_pay", "estimated_cac", "monthly_leads")
    @classmethod
    def validate_non_negative(cls, value: float | int) -> float | int:
        if value < 0:
            raise ValueError("must be non-negative")
        return value


class ProjectionResponse(BaseModel):
    """Strict output returned by the model-generation endpoint."""

    model_config = ConfigDict(extra="forbid")

    monthly_mrr: list[float] = Field(min_length=12, max_length=12)
    cac_payback_period_months: float | None = Field(default=None, ge=0)
    ltv: float = Field(ge=0)
    extracted_signals: ExtractedSignals
