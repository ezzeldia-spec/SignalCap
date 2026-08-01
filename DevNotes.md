# SignalCap

SignalCap converts qualitative interview transcripts into deterministic SaaS financial models.

## Architecture

- `signalcap.schemas`: validated request, extraction, and response contracts.
- `signalcap.extraction`: isolated probabilistic LLM boundary.
- `signalcap.finance`: deterministic financial model boundary.
- `signalcap.api`: FastAPI transport and orchestration boundary.

The scaffold intentionally contains no extraction or financial-calculation implementation yet.
