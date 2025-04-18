import json
from app.services.llm_client import query_llm

def extract_user_info(summary: str) -> dict:
    """
    Extracts structured user information from a human-readable summary.
    Returns a JSON object with keys:
      full_name, id_number, gender, age, hmo_name, hmo_card_number, insurance_membership_tier.
    Fields that are missing or unclear are set to null.
    Ignores any clarifying questions in the summary and outputs only the JSON.
    """
    system = (
        "You are a JSON extractor. "
        "The user summary follows this pattern:\n"
        "Full name: <value>\n"
        "ID number: <value>\n"
        "Gender: <value>\n"
        "Age: <value>\n"
        "HMO name: <value>\n"
        "HMO card number: <value>\n"
        "Insurance membership tier: <value>\n\n"
        "The summary may include clarifying questions like “Did you mean …?”. "
        "Ignore those. Output ONLY a JSON object with keys: "
        "full_name, id_number, gender, age, hmo_name, "
        "hmo_card_number, insurance_membership_tier. "
        "If you can’t determine a field, use null. "
        "No extra text."
    )
    resp = query_llm(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": summary}
        ],
        temperature=0.0
    ).strip()
    return json.loads(resp)
