import pytest

from signalcap.extraction.service import SignalExtractionService
from signalcap.finance.model import SaaSFinancialModel
from signalcap.schemas import ExtractedSignals


@pytest.mark.asyncio
async def test_extraction_service_is_an_async_unimplemented_boundary() -> None:
    with pytest.raises(NotImplementedError):
        await SignalExtractionService().extract("Interview transcript")


def test_financial_model_is_constructed_from_validated_signals() -> None:
    signals = ExtractedSignals(
        willingness_to_pay=100.0,
        estimated_cac=250.0,
        monthly_churn_percentage=0.05,
        expected_conversion_rate=0.1,
        monthly_leads=50,
    )

    assert SaaSFinancialModel(signals).signals is signals
