from pathlib import Path
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routes import (
    affiliate,
    agents,
    ai,
    content,
    database,
    ethical,
    market,
    profile,
    reports,
    validation,
)


app = FastAPI(
    title="CreatorCareer AI Backend",
    description=(
        "Clean FastAPI backend for CreatorCareer AI. "
        "This backend includes modular routes, Supabase database layer, "
        "IBM Granite/Ollama-ready AI layer, 7-agent dashboard, "
        "ethical monetization checker, and PDF report generator."
    ),
    version="1.1.0",
)


def get_allowed_origins() -> list[str]:
    """
    Production-safe CORS origin loader.

    This allows:
    - Local frontend during development
    - Vercel production frontend
    - Extra frontend URLs from Render environment variable FRONTEND_URL

    FRONTEND_URL can contain one URL or multiple comma-separated URLs:
    FRONTEND_URL=http://localhost:3000,https://creator-career-ai.vercel.app
    """

    default_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://creator-career-ai.vercel.app",
    ]

    frontend_url_env = os.getenv("FRONTEND_URL", "")

    env_origins = [
        origin.strip().rstrip("/")
        for origin in frontend_url_env.split(",")
        if origin.strip()
    ]

    # Remove duplicates while keeping order.
    return list(dict.fromkeys(default_origins + env_origins))


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Generated PDF reports are saved inside backend/reports
# and served publicly from:
# https://creatorcareer-ai.onrender.com/reports/<file-name>.pdf
reports_dir = Path(__file__).parent / "reports"
reports_dir.mkdir(exist_ok=True)

app.mount("/reports", StaticFiles(directory=str(reports_dir)), name="reports")


# Register all API routers.
# These keep the existing frontend endpoint URLs stable.
app.include_router(profile.router)
app.include_router(content.router)
app.include_router(market.router)
app.include_router(validation.router)
app.include_router(affiliate.router)
app.include_router(ethical.router)
app.include_router(agents.router)
app.include_router(reports.router)
app.include_router(database.router)
app.include_router(ai.router)


@app.get("/")
def root_health_check():
    """
    Simple backend health check.
    """

    return {
        "status": "ok",
        "message": "CreatorCareer AI backend is running",
        "version": "1.1.0",
        "ai_engine": "local_explainable_ai",
    }


@app.head("/")
def root_head_check():
    """
    Render sometimes sends HEAD request for service checking.
    This avoids unnecessary 405 Method Not Allowed logs.
    """

    return None


@app.get("/health")
def health_alias():
    """
    Extra health route for deployment platforms and manual testing.
    """

    return {
        "status": "ok",
        "message": "CreatorCareer AI backend health check passed",
        "version": "1.1.0",
    }


@app.get("/cors-debug")
def cors_debug():
    """
    Temporary debug route.
    Use this to confirm which frontend URLs are allowed in production.
    """

    return {
        "allowed_origins": get_allowed_origins(),
        "frontend_url_env": os.getenv("FRONTEND_URL", "NOT SET"),
        "note": "If your Vercel frontend URL is inside allowed_origins, CORS should work after Render redeploy.",
    }


