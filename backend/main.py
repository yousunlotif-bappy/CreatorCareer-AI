from pathlib import Path

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
        "This version includes the modular route structure, Supabase database layer, "
        "IBM Granite local AI layer, 7-agent dashboard, and PDF report generator."
    ),
    version="1.0.0",
)


# Allow the local Next.js frontend to call the FastAPI backend.
# Keep this origin for local development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Generated PDF reports are saved inside backend/reports
# and served publicly from http://localhost:8000/reports/<file-name>.pdf
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
def health_check():
    """
    Simple backend health check.
    """

    return {
        "status": "ok",
        "message": "CreatorCareer AI backend is running",
        "version": "1.1.0",
        "ai_engine": "local_explainable_ai",
    }


