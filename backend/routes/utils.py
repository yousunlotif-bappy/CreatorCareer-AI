from typing import Optional

from services.database import insert_record


def clean_optional_uuid(value: Optional[str]) -> Optional[str]:
    """
    Convert empty UUID strings into None.

    Supabase uuid columns reject empty strings, so this helper prevents
    common insert errors when creator_id is not available yet.
    """

    if value and value.strip():
        return value.strip()

    return None


def extract_inserted_id(saved_record) -> Optional[str]:
    """
    Safely extract inserted row id from different Supabase response shapes.
    """

    if not isinstance(saved_record, dict):
        return None

    saved_data = saved_record.get("data")

    if isinstance(saved_data, list) and saved_data:
        first_row = saved_data[0]

        if isinstance(first_row, dict):
            return first_row.get("id")

    if isinstance(saved_data, dict):
        return saved_data.get("id")

    return saved_record.get("id")


def save_record_safely(table_name: str, payload: dict) -> dict:
    """
    Save a record to Supabase without breaking the main API response.

    The app still returns generated output even if database saving fails
    because of a missing table, missing column, or wrong column type.
    """

    try:
        saved_record = insert_record(table_name, payload)

        return {
            "database_saved": True,
            "database_record": saved_record,
            "database_record_id": extract_inserted_id(saved_record),
            "database_error": None,
        }

    except Exception as error:
        return {
            "database_saved": False,
            "database_record": None,
            "database_record_id": None,
            "database_error": str(error),
        }


def attach_database_result(result: dict, db_result: dict) -> dict:
    """
    Add database status fields to any API response.
    """

    result["database_saved"] = db_result["database_saved"]
    result["database_record_id"] = db_result["database_record_id"]
    result["database_error"] = db_result["database_error"]

    return result




