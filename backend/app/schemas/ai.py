from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    context: str = "general" # inventory, orders, analytics

class ChatResponse(BaseModel):
    response: str
    actions: list = [] # Suggested actions (e.g. "Create Order", "View Report")
