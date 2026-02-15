from fastapi import FastAPI, Body
from app.services.logic import AIService
from pydantic import BaseModel

app = FastAPI(title="AI Service")

class ChatRequest(BaseModel):
    message: str
    context: str = ""

@app.post("/api/v1/ai/chat")
async def chat(request: ChatRequest):
    service = AIService()
    return await service.chat(request.message, request.context)

@app.get("/health")
def health():
    return {"status": "ok"}
