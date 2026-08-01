"""LLM-backed structured extraction; no financial calculations belong here."""

import json

from openai import AsyncOpenAI
from pydantic import ValidationError

from signalcap.schemas import ExtractedSignals


class SignalExtractionError(RuntimeError):
    """The LLM could not provide a complete, schema-valid extraction."""


class SignalExtractionService:
    """Translate transcript text into schema-validated commercial signals."""

    def __init__(self, client: AsyncOpenAI | None = None, model: str = "gpt-4o-mini") -> None:
        self._client = client or AsyncOpenAI()
        self._model = model

    async def extract(self, transcript: str) -> ExtractedSignals:
        """Request schema-constrained facts and validate their JSON response."""
        if not transcript or not transcript.strip():
            raise SignalExtractionError("Transcript must not be empty")
        try:
            completion = await self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": (
                        "Extract only the requested commercial facts from the interview. "
                        "Do not calculate, estimate through arithmetic, or produce financial projections. "
                        "Rates must be decimal fractions between 0 and 1."
                    )},
                    {"role": "user", "content": transcript},
                ],
                response_format={"type": "json_schema", "json_schema": {
                    "name": "extracted_signals", "strict": True,
                    "schema": ExtractedSignals.model_json_schema(),
                }},
            )
            content = completion.choices[0].message.content
            if not content:
                raise SignalExtractionError("LLM returned no structured extraction")
            return ExtractedSignals.model_validate(json.loads(content))
        except SignalExtractionError:
            raise
        except (IndexError, KeyError, TypeError, json.JSONDecodeError, ValidationError) as exc:
            raise SignalExtractionError("LLM returned malformed extraction data") from exc
        except Exception as exc:
            raise SignalExtractionError("LLM extraction request failed") from exc
