import httpx
from app.core.config import settings
from app.schemas.ai import ChatResponse

class AIService:
    def __init__(self):
        self.api_key = settings.AI_API_KEY
        self.model = settings.AI_MODEL
        self.base_url = "https://openrouter.ai/api/v1"

    async def chat(self, message: str, context: str) -> ChatResponse:
        if not self.api_key:
            return ChatResponse(response="AI is disabled (API Key missing).", actions=[])

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            # "HTTP-Referer": "http://localhost:3000", # Optional for OpenRouter
        }

        system_prompt = (
            "You are an intelligent business assistant for an Inventory Management System. "
            "Help the user with questions about stock, orders, and business health. "
            f"Context: {context}. "
            "Keep answers professional, concise, and format data clearly."
            "Use values and symbols relevant to India (₹)."
        )

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                content = data['choices'][0]['message']['content']
                return ChatResponse(response=content)
        except Exception as e:
            return ChatResponse(response=f"I encountered an error connecting to my brain: {str(e)}")
