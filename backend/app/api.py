from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm_client import ask_llm

router = APIRouter()

class ChatRequest(BaseModel):
    phase: str
    user_info: dict
    messages: list

@router.post("/chat")
async def chat(payload: ChatRequest):
    response = ask_llm(payload.phase, payload.user_info, payload.messages)
    return {"response": response}
