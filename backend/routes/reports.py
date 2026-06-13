import re
import uuid
from pathlib import Path

from fastapi import APIRouter

from models.schemas import ReportGenerateRequest
from routes.utils import attach_database_result, clean_optional_uuid, save_record_safely
from services.ai_service import generate_local_ai_response
from services.report_generator import generate_pdf_report


router = APIRouter(prefix="/report", tags=["Reports"])


def clean_file_part(value: str) -> str:
    """
    Convert user text into a safe filename part.
    """

    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    cleaned = cleaned.strip("-")

    return cleaned or "creator"


@router.post("/generate")
def generate_report(request: ReportGenerateRequest):
    """
    Generate a PDF report, add local AI response metadata, and save report history.
    """

    reports_dir = Path(__file__).resolve().parents[1] / "reports"
    reports_dir.mkdir(exist_ok=True)

    safe_name = clean_file_part(request.creator_name)
    file_name = f"creatorcareer-report-{safe_name}-{uuid.uuid4().hex[:8]}.pdf"
    file_path = reports_dir / file_name

    generate_pdf_report(request, file_path)

    download_url = f"http://localhost:8000/reports/{file_name}"

    result = {
        "status": "success",
        "message": "PDF report generated successfully.",
        "file_name": file_name,
        "download_url": download_url,
    }

    result.update(
        generate_local_ai_response(
            module_name="report",
            payload={
                "creator_name": request.creator_name,
                "creator_niche": request.creator_niche,
                "audience": request.audience,
                "region": request.region,
                "platforms": request.platforms,
                "product_idea": request.product_idea,
                "business_model": request.business_model,
                "income_goal": request.income_goal,
            },
        )
    )

    database_payload = {
        "creator_id": clean_optional_uuid(request.creator_id),
        "creator_name": request.creator_name,
        "creator_niche": request.creator_niche,
        "audience": request.audience,
        "region": request.region,
        "platforms": request.platforms,
        "product_idea": request.product_idea,
        "business_model": request.business_model,
        "income_goal": request.income_goal,
        "overall_business_opportunity_score": 84,
        "report_file_name": file_name,
        "report_download_url": download_url,
    }

    db_result = save_record_safely("reports", database_payload)

    return attach_database_result(result, db_result)


