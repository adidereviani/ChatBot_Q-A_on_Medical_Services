import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ValidationError, validator
from typing import List, Dict, Any

from app.services.info_collector import collect_user_info
from app.services.user_info_extractor import extract_user_info
from app.services.qa_handler import answer_question
from app.services.confirm_classifier import is_confirmation
from app.utils.logger import logger

# Initialize FastAPI router
router = APIRouter()

class ChatMessage(BaseModel):
    """
    Represents a single chat message with a role and content.
    """
    role: str
    content: str

class ChatRequest(BaseModel):
    """
    Represents the incoming chat request payload.
    Includes conversation phase, user info, and messages.
    """
    phase: str
    user_info: Dict[str, Any]
    messages: List[ChatMessage]

    @validator("phase")
    def validate_phase(cls, v):
        """
        Validates that the phase is either 'info_collection' or 'qa'.
        """
        if v not in ("info_collection", "qa"):
            raise ValueError("phase must be 'info_collection' or 'qa'")
        return v


@router.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    """
    Chat endpoint that handles info collection and question answering phases.
    Depending on the phase, it interacts with the LLM to either collect information
    or answer user queries based on provided personal details.
    """
    try:
        msgs = [m.dict() for m in payload.messages]

        if payload.phase == "info_collection":
            reply = collect_user_info(msgs)

            if len(payload.messages) >= 8 and is_confirmation(payload.messages[-1].content):
                last_bot = next(m["content"] for m in reversed(msgs) if m["role"] == "assistant")
                try:
                    user_info = extract_user_info(last_bot)
                    next_phase = "qa"
                    reply = answer_question(user_info, msgs)
                except Exception:
                    user_info = payload.user_info
                    next_phase = "info_collection"
            else:
                user_info = payload.user_info
                next_phase = "info_collection"

        else:
            user_info = payload.user_info
            reply = answer_question(user_info, msgs)
            next_phase = None

        return {"response": reply, "next_phase": next_phase, "user_info": user_info}

    except ValidationError as ve:
        logger.error(f"Validation Error: {ve}")
        raise HTTPException(422, str(ve))
    except ValueError as ve:
        logger.error(f"Value Error: {ve}")
        raise HTTPException(400, str(ve))
    except Exception as e:
        logger.exception("Unhandled exception")
        raise HTTPException(500, "Internal Server Error")
