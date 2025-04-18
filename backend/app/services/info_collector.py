from app.services.llm_client import query_llm

def build_info_prompt() -> str:
    """
    Constructs the system prompt for the LLM to collect user medical information.
    """
    return (
        "You are a helpful medical assistant. Always respond in the same language the user uses.\n"
        "Support both Hebrew and English and respond in the user's language.\n"
        "Begin the conversation by asking: 'How can I assist you today?'\n"
        "Only collect personal information if the user asks about medical services or health insurance.\n"
        "If relevant, ask conversationally for the following details:\n"
        "- Full name\n"
        "- ID number (9 digits)\n"
        "- Gender\n"
        "- Age (0-120)\n"
        "- HMO name (מכבי | מאוחדת | כללית — Maccabi | Meuhedet | Clalit)\n"
        "- HMO card number (9 digits)\n"
        "- Insurance membership tier (זהב | כסף | ארד — Gold | Silver | Bronze)\n"
        "Always ask each question separately; never ask all the questions at once.\n"
        "Do not ask for any personal info unless it's needed to help them.\n"
        "Once all details are collected, you MUST confirm them clearly and politely.\n"
        "When confirming the information, list each item on a new line. Use line breaks (\\n) between each detail for clarity.\n"
    )

def collect_user_info(messages: list) -> str:
    """
    Sends the conversation history to the LLM wrapped with the system prompt for information collection.
    """
    system = build_info_prompt()
    print(f"system_prompt: {system}")
    return query_llm([{"role": "system", "content": system}] + messages, temperature=0.5)
