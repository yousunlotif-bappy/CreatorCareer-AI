"""
Route Utility Helpers

Shared helper functions for:
- Cleaning optional UUID values
- Saving records safely to Supabase
- Extracting database record IDs
- Attaching database status to API responses
- Providing database proof values for frontend proof cards
"""

from typing import Any, Optional
from uuid import UUID

from services.database import insert_record


def clean_optional_uuid(value: Optional[str]) -> Optional[str]:
    """
    Convert empty or invalid UUID strings into None.

    Supabase UUID columns reject empty strings.
    This helper prevents common insert errors when creator_id is not available yet.
    """

    if not value:
        return None

    cleaned_value = value.strip()

    if not cleaned_value:
        return None

    try:
        UUID(cleaned_value)
        return cleaned_value
    except ValueError:
        return None


def extract_inserted_id(saved_record: Any) -> Optional[str]:
    """
    Safely extract inserted row id from different Supabase response shapes.
    """

    try:
        if not saved_record:
            return None

        if isinstance(saved_record, dict):
            if saved_record.get("id"):
                return str(saved_record["id"])

            saved_data = saved_record.get("data")

            if isinstance(saved_data, list) and saved_data:
                first_row = saved_data[0]

                if isinstance(first_row, dict) and first_row.get("id"):
                    return str(first_row["id"])

            if isinstance(saved_data, dict) and saved_data.get("id"):
                return str(saved_data["id"])

            database_record = saved_record.get("database_record")

            if isinstance(database_record, dict):
                return extract_inserted_id(database_record)

            record = saved_record.get("record")

            if isinstance(record, dict) and record.get("id"):
                return str(record["id"])

        saved_data = getattr(saved_record, "data", None)

        if isinstance(saved_data, list) and saved_data:
            first_row = saved_data[0]

            if isinstance(first_row, dict) and first_row.get("id"):
                return str(first_row["id"])

        if isinstance(saved_data, dict) and saved_data.get("id"):
            return str(saved_data["id"])

        record_id = getattr(saved_record, "id", None)

        if record_id:
            return str(record_id)

        return None

    except Exception:
        return None


def save_record_safely(table_name: str, payload: dict[str, Any]) -> dict[str, Any]:
    """
    Save a record to Supabase without breaking the main API response.

    The app still returns generated output even if database saving fails
    because of a missing table, missing column, or wrong column type.
    """

    try:
        saved_record = insert_record(table_name, payload)
        database_record_id = extract_inserted_id(saved_record)

        return {
            "database_saved": True,
            "database_record": saved_record,
            "database_record_id": database_record_id,
            "database_error": None,
        }

    except Exception as error:
        return {
            "database_saved": False,
            "database_record": None,
            "database_record_id": None,
            "database_error": str(error),
        }


def is_database_saved(db_result: dict[str, Any]) -> bool:
    """
    Return safe database saved status.
    """

    if not isinstance(db_result, dict):
        return False

    return bool(db_result.get("database_saved"))


def get_database_record_id(db_result: dict[str, Any]) -> str:
    """
    Return database record id as a string.
    """

    if not isinstance(db_result, dict):
        return ""

    record_id = db_result.get("database_record_id")

    if record_id:
        return str(record_id)

    database_record = db_result.get("database_record")
    extracted_id = extract_inserted_id(database_record)

    return extracted_id or ""


def attach_database_result(
    result: dict[str, Any],
    db_result: dict[str, Any],
) -> dict[str, Any]:
    """
    Add database status fields to any API response.
    """

    result["database_saved"] = is_database_saved(db_result)
    result["database_record_id"] = get_database_record_id(db_result)
    result["database_error"] = (
        db_result.get("database_error")
        if isinstance(db_result, dict)
        else "Invalid database result."
    )

    return result


def get_database_proof_values(db_result: dict[str, Any]) -> dict[str, Any]:
    """
    Return database proof values for add_proof_fields().

    Used by backend routes before returning response to frontend.
    """

    return {
        "database_saved": is_database_saved(db_result),
        "database_record_id": get_database_record_id(db_result),
    }


