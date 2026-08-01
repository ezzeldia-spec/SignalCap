"""FastAPI dependency providers."""

from signalcap.extraction import SignalExtractionService


def get_extraction_service() -> SignalExtractionService:
    return SignalExtractionService()
