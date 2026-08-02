"""FastAPI dependency providers."""

from signalcap.extraction import SignalExtractor


def get_signal_extractor() -> SignalExtractor:
    return SignalExtractor()
