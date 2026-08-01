"""SignalCap ASGI application."""

from fastapi import FastAPI

from signalcap.api.routes import router

app = FastAPI(title="SignalCap", version="0.1.0")
app.include_router(router)
