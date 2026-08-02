import json
from types import SimpleNamespace

import pytest

from signalcap.extraction import ExtractionError, SignalExtractor


class FakeCompletions:
    def __init__(self, content: str | None) -> None:
        self.content = content
        self.calls: list[dict[str, object]] = []

    async def create(self, **kwargs: object) -> SimpleNamespace:
        self.calls.append(kwargs)
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=self.content))])


def fake_client(content: str | None) -> tuple[SimpleNamespace, FakeCompletions]:
    completions = FakeCompletions(content)
    return SimpleNamespace(chat=SimpleNamespace(completions=completions)), completions


@pytest.mark.asyncio
async def test_extract_uses_strict_structured_output_without_math() -> None:
    client, completions = fake_client(json.dumps({
        "willingness_to_pay": 99.0, "estimated_cac": 250.0,
        "monthly_churn_percentage": 0.02, "expected_conversion_rate": 0.15, "monthly_leads": 30,
    }))
    signals = await SignalExtractor(client=client).extract("Customers said they would pay $99.")  # type: ignore[arg-type]
    assert signals.willingness_to_pay == 99
    request = completions.calls[0]
    response_format = request["response_format"]  # type: ignore[index]
    assert response_format["json_schema"]["strict"] is True  # type: ignore[index]
    assert "Do not calculate" in request["messages"][0]["content"]  # type: ignore[index]


@pytest.mark.asyncio
@pytest.mark.parametrize("content", [None, "not-json", '{"monthly_leads": 10}'])
async def test_extract_maps_bad_output_to_domain_error(content: str | None) -> None:
    client, _ = fake_client(content)
    with pytest.raises(ExtractionError):
        await SignalExtractor(client=client).extract("Interview")  # type: ignore[arg-type]
