"""HTTP routes for financial-model generation."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from signalcap.api.dependencies import get_extraction_service
from signalcap.extraction import SignalExtractionError, SignalExtractionService
from signalcap.finance import SaaSFinancialModel
from signalcap.schemas import InterviewTranscript, ProjectionResponse

router = APIRouter(prefix="/api/v1", tags=["models"])


@router.post("/generate-model", response_model=ProjectionResponse)
async def generate_model(
    payload: InterviewTranscript,
    extractor: Annotated[SignalExtractionService, Depends(get_extraction_service)],
) -> ProjectionResponse:
    """Extract signals, then calculate results only in the deterministic layer."""
    try:
        signals = await extractor.extract(payload.transcript)
    except SignalExtractionError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Unable to extract a complete financial model from transcript.",
        ) from exc
    model = SaaSFinancialModel(signals)
    return ProjectionResponse(
        signals=signals,
        monthly_projection=model.project_12_months(),
        cac_payback_period_months=model.cac_payback_period_months(),
        lifetime_value=model.lifetime_value(),
    )
