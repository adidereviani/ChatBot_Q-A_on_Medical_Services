import os
from openai import AzureOpenAI
from app.services.info_collector import build_info_prompt
from app.utils.html_loader import get_all_html_text
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_API_BASE")
)


def ask_llm(phase, user_info, messages):
    if phase == "info_collection":
        system_prompt = build_info_prompt()
    elif phase == "qa":
        base_prompt = (
            f"You are a helpful medical assistant for {user_info['HMO name']} "
            f"members with {user_info['Insurance membership tier']} insurance.\n"
            "You understand both Hebrew and English and will respond in the language the user writes in.\n"
            "Answer based ONLY on the data below.\n"
        )
        knowledge_base = get_all_html_text()
        system_prompt = base_prompt + "\n\nUse the following medical services data:\n" + knowledge_base
    else:
        raise ValueError("Invalid phase")

    chat_messages = [{"role": "system", "content": system_prompt}] + messages

    response = client.chat.completions.create(
        model=os.getenv("AZURE_DEPLOYMENT_NAME"),
        messages=chat_messages,
        temperature=0.5
    )

    return response.choices[0].message.content
