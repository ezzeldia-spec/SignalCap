import pytest
from httpx import ASGITransport, AsyncClient

from signalcap.api.dependencies import get_signal_extractor
from signalcap.extraction import ExtractionError
from signalcap.main import create_app
from signalcap.schemas import ExtractedSignals


class StubExtractor:
    async def extract(self, transcript: str) -> ExtractedSignals:
        assert transcript == "Interview content"
        return ExtractedSignals(willingness_to_pay=100, estimated_cac=300,
            monthly_churn_percentage=0.1, expected_conversion_rate=0.1, monthly_leads=100)


class FailingExtractor:
    async def extract(self, transcript: str) -> ExtractedSignals:
        raise ExtractionError("bad extraction")


@pytest.mark.asyncio
async def test_generate_model_orchestrates_mocked_extraction_and_finance() -> None:
    app = create_app()
    app.dependency_overrides[get_signal_extractor] = lambda: StubExtractor()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/generate-model", json={"transcript": "Interview content"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["monthly_mrr"][:2] == [1000.0, 1900.0]
    assert payload["cac_payback_period_months"] == 3.0
    assert payload["ltv"] == 1000.0
    assert payload["extracted_signals"]["monthly_leads"] == 100


@pytest.mark.asyncio
async def test_generate_model_returns_422_when_extraction_fails() -> None:
    app = create_app()
    app.dependency_overrides[get_signal_extractor] = lambda: FailingExtractor()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/generate-model", json={"transcript": "x"})
    assert response.status_code == 422
