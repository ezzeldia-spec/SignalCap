"""LLM-backed extraction service interface.

This module is the only layer permitted to interact with an LLM SDK. It must
return a validated ``ExtractedSignals`` instance and never perform financial
calculations.
"""

from signalcap.schemas import ExtractedSignals


class SignalExtractionError(RuntimeError):
    """Raised when structured LLM extraction is missing or malformed."""


class SignalExtractionService:
    """Asynchronous port for structured interview-signal extraction."""

    async def extract(self, transcript: str) -> ExtractedSignals:
        """Extract validated signals from raw transcript text.

        TODO: Add OpenAI structured-output/tool-calling integration and map
        malformed or incomplete model output to ``SignalExtractionError``.
        """
        raise NotImplementedError("LLM extraction has not been implemented yet")
