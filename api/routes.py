"""HTTP routes for financial model generation."""

from fastapi import APIRouter, HTTPException, status

from signalcap.schemas import InterviewTranscript, ProjectionResponse

router = APIRouter(prefix="/api/v1", tags=["models"])


@router.post(
    "/generate-model",
    response_model=ProjectionResponse,
    status_code=status.HTTP_200_OK,
)
async def generate_model(payload: InterviewTranscript) -> ProjectionResponse:
    """Orchestrate extraction and deterministic projection (pending implementation)."""
    del payload
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Model generation has not been implemented yet.",
    )
