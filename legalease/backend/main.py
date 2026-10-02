"""
LegalEase FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import router


APP_NAME = "LegalEase"
APP_VERSION = "1.0.0"


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="AI-powered legal document draft generator.",
)


# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API routes
app.include_router(router)


@app.get("/")
def home():
    return {
        "status": "ok",
        "service": APP_NAME,
        "version": APP_VERSION,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }