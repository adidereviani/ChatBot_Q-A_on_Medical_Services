import re
from app.services.llm_client import query_llm

def parse_confirmation_response(resp: str) -> bool:
    """
    Parses the LLM's raw text response for confirmation.
    Returns True if the response is exactly 'yes' (ignoring case and punctuation), otherwise False.
    """
    clean = resp.strip().lower().rstrip(".!?")
    return clean == "yes"

def is_confirmation(user_msg: str) -> bool:
    """
    Determines if the user's message is a confirmation using the LLM.
    Returns True if the LLM classifies the message as a confirmation, otherwise False.
    """
    system = (
        "You are a binary classifier. Reply ONLY 'yes' or 'no'.\n\n"
        "If the user clearly confirms all the personal info "
        "(using words like 'yes', 'right', 'correct', 'confirmed', 'נכון', etc.), reply 'yes'.\n"
        "Reply 'no' for corrections, clarifications, uncertainty, or anything else.\n"
        "Always infer meaning, not exact wording."
    )
    user = f"\"{user_msg}\""
    resp = query_llm(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        temperature=0.0
    ).strip().lower()
    return parse_confirmation_response(resp)
