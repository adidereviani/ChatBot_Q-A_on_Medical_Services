import os
from openai import AzureOpenAI
from dotenv import load_dotenv

from app.services.info_collector import build_info_prompt
from app.utils.html_loader import get_all_html_text
from app.utils.logger import logger

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_API_BASE")
)

def ask_llm(phase, user_info, messages):
    """
    Takes the phase, user_info, and conversation messages from the client,
    builds a system prompt, and queries Azure OpenAI for a response.
    """
    try:
        if phase == "info_collection":
            system_prompt = build_info_prompt()
        elif phase == "qa":
            base_prompt = (
                f"You are a helpful medical assistant for {user_info['HMO name']} "
                f"members with {user_info['Insurance membership tier']} insurance.\n"
                "You understand both Hebrew and English and will respond in the language the user writes in.\n"
                "Only answer based on the exact data provided below.\n"
                "Do not guess, invent, or assume details that are not listed.\n"
                "Format your answer clearly and directly. For example:\n"
                "'ההנחה עבור סתימה במכבי זהב היא 80%.'\n"
                "If no match is found, respond: 'I could not find this information.'\n"
            )
            knowledge_base = get_all_html_text()
            system_prompt = base_prompt + "\n\nUse the following medical services data:\n" + knowledge_base
        else:
            raise ValueError(f"Invalid phase: {phase}")

        chat_messages = [{"role": "system", "content": system_prompt}] + messages

        logger.info(f"Sending ChatCompletion request | Phase={phase} | System prompt snippet: {system_prompt[:100]}...")

        response = client.chat.completions.create(
            model=os.getenv("AZURE_DEPLOYMENT_NAME"),
            messages=chat_messages,
            temperature=0.5
        )

        answer = response.choices[0].message.content
        logger.info(f"Received ChatCompletion answer: {answer[:100]}...")

        return answer

    except Exception as e:
        logger.exception("Error in ask_llm")
        raise e

