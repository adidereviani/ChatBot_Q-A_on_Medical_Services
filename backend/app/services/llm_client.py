import os
from openai import AzureOpenAI
from app.services.qa_handler import get_context_from_html
from app.services.info_collector import build_info_prompt

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
        system_prompt = (
            f"You are a helpful medical assistant for {user_info['HMO name']} "
            f"members with {user_info['Insurance membership tier']} insurance.\n"
        )
        system_prompt += get_context_from_html(user_info["HMO name"], user_info["Insurance membership tier"])
    else:
        raise ValueError("Invalid phase")

    chat_messages = [{"role": "system", "content": system_prompt}] + messages

    response = client.chat.completions.create(
        model=os.getenv("AZURE_DEPLOYMENT_NAME"),
        messages=chat_messages,
        temperature=0.5
    )

    return response.choices[0].message.content
