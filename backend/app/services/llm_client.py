import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from app.utils.logger import logger

load_dotenv()

# Initialize the Azure OpenAI client with environment variables
_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_API_BASE")
)

# Set the model deployment name
_MODEL = os.getenv("AZURE_DEPLOYMENT_NAME")

def query_llm(messages: list, temperature: float = 0.5) -> str:
    """
    Generic chat-completion wrapper to query Azure OpenAI.
    Logs full prompt and response for debugging.
    """
    try:
        logger.info("Calling LLM...")
        for msg in messages:
            logger.info(f"{msg['role'].upper()}: {msg['content']}")

        resp = _client.chat.completions.create(
            model=_MODEL,
            messages=messages,
            temperature=temperature
        )

        text = resp.choices[0].message.content

        logger.info(f"LLM response:\n{text}")

        return text

    except Exception as e:
        logger.exception("Error during LLM call")
        raise e
