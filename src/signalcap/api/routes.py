"""HTTP routes for financial-model generation."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from signalcap.api.dependencies import get_signal_extractor
from signalcap.extraction import ExtractionError, SignalExtractor
from signalcap.finance import SaaSFinancialModel
from signalcap.schemas import InterviewTranscript, ProjectionResponse

router = APIRouter(prefix="/api/v1", tags=["models"])


@router.post("/generate-model", response_model=ProjectionResponse)
async def generate_model(
    payload: InterviewTranscript,
    extractor: Annotated[SignalExtractor, Depends(get_signal_extractor)],
) -> ProjectionResponse:
    """Extract signals, then calculate results only in the deterministic layer."""
    try:
        signals = await extractor.extract(payload.transcript)
    except (ExtractionError, ValidationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Unable to extract a complete financial model from transcript.",
        ) from exc
    return SaaSFinancialModel(signals).generate_projection()
