from fastapi import APIRouter, Depends, HTTPException
from app.services.ai_service import AIService
from app.schemas.ai import ChatRequest, ChatResponse

router = APIRouter()

def get_service() -> AIService:
    return AIService()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest, service: AIService = Depends(get_service)):
    return await service.chat(request.message, request.context)
