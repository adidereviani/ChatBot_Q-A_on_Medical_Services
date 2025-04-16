from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ValidationError, validator
from typing import List, Dict, Any

from app.services.llm_client import ask_llm
from app.utils.logger import logger

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    phase: str
    user_info: Dict[str, Any]
    messages: List[ChatMessage]

    @validator("phase")
    def validate_phase(cls, v):
        if v not in ("info_collection", "qa"):
            raise ValueError("phase must be 'info_collection' or 'qa'")
        return v


@router.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    """
    Receives:
    {
      "phase": "info_collection" or "qa",
      "user_info": {...},
      "messages": [{"role": "user"|"assistant", "content": "..."}, ...]
    }

    Returns a JSON response: {"response": "..."}
    """
    # Log the inbound request
    logger.info(f"Incoming chat request | phase={payload.phase} | user_info={payload.user_info}")

    try:
        # The server does not store user state.
        # All session data is from the client (payload).
        response_text = ask_llm(payload.phase, payload.user_info, [msg.dict() for msg in payload.messages])
        # Log the outbound response
        logger.info(f"Chat response: {response_text[:200]}...")  # partial to avoid huge logs
        return {"response": response_text}
    except ValidationError as ve:
        logger.error(f"Validation Error: {ve}")
        raise HTTPException(status_code=422, detail=str(ve))
    except ValueError as ve:
        logger.error(f"Value Error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.exception("Unhandled exception during chat request")
        raise HTTPException(status_code=500, detail="Internal Server Error")
