import json
import os
from app.utils.html_loader import get_all_html_text
from app.services.llm_client import query_llm

def build_qa_prompt(user_info: dict, knowledge_base: str) -> str:
    """
    Constructs the system prompt for answering user questions based on personal info and knowledge base.
    """
    return (
        "You are a helpful medical assistant.\n"
        "You assist users based on their personal details and insurance information.\n"
        "The user info is:\n"
        f"{json.dumps(user_info, ensure_ascii=False, indent=2)}\n\n"
        "You understand both Hebrew and English and will respond in the language the user writes in.\n"
        "Only answer based on the exact data provided below.\n"
        "Do not guess, invent, or assume any details beyond what is given.\n"
        "Format your answer clearly and directly.\n"
        "If no match is found, respond: 'I could not find this information.'\n\n"
        "Use the following medical services data:\n"
        f"{knowledge_base}"
    )

def answer_question(user_info: dict, messages: list) -> str:
    """
    Sends the user's info and conversation to the LLM for a knowledge-based answer.
    """
    kb = get_all_html_text()
    system = build_qa_prompt(user_info, kb)
    print(f"system_prompt: {system}")
    return query_llm([{"role": "system", "content": system}] + messages, temperature=0.5)
