import re
import uuid
from pathlib import Path

from fastapi import APIRouter

from models.schemas import ReportGenerateRequest
from routes.utils import (
    attach_database_result,
    clean_optional_uuid,
    get_database_proof_values,
    save_record_safely,
)
from services.ai_service import generate_local_ai_response
from services.proof import add_proof_fields
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
    Generate a PDF report, add local AI response metadata,
    save report history, and return correct proof fields.
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

    ai_result = generate_local_ai_response(
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

    result.update(ai_result)

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

    response_payload = attach_database_result(result, db_result)
    proof_values = get_database_proof_values(db_result)

    return add_proof_fields(
        payload=response_payload,
        database_saved=proof_values["database_saved"],
        database_record_id=proof_values["database_record_id"],
        granite_used=True,
    )

