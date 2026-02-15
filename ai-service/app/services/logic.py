import httpx
from app.core.config import settings
import json

class AIService:
    def __init__(self):
        self.api_key = settings.AI_API_KEY
        self.model = settings.AI_MODEL
        self.base_url = "https://openrouter.ai/api/v1"

    async def _fetch_inventory_context(self):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(settings.INVENTORY_SERVICE_URL)
                if resp.status_code == 200:
                    products = resp.json()
                    # Summarize for token efficiency
                    summary = []
                    for p in products:
                        summary.append(f"- {p['name']}: {p['stock_quantity']} units (Price: ${p['price']})")
                    return "\n".join(summary)
        except Exception as e:
            print(f"Error fetching inventory: {e}")
        return "Inventory data unavailable."

    async def _fetch_analytics_context(self):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{settings.ANALYTICS_SERVICE_URL}/dashboard")
                if resp.status_code == 200:
                    data = resp.json()
                    return json.dumps(data, indent=2)
        except Exception as e:
            print(f"Error fetching analytics: {e}")
        return "Analytics data unavailable."

    async def chat(self, message: str, context: str = ""):
        if not self.api_key:
            return {"response": "AI Service not configured (Missing API Key)."}

        # 1. Fetch Real-Time Context (RAG)
        inventory_data = await self._fetch_inventory_context()
        analytics_data = await self._fetch_analytics_context()

        system_prompt = f"""You are a helpful business assistant for an Inventory Management System. 
        You have access to the following REAL-TIME business data:
        
        === EXISTING INVENTORY ===
        {inventory_data}
        
        === DASHBOARD METRICS ===
        {analytics_data}
        
        INSTRUCTIONS:
        - Answer the user's question based on the data above.
        - If the user asks about low stock, check the 'stock_quantity'. Assume < 10 is low stock unless specified.
        - If the user asks about revenue, look at the dashboard metrics.
        - Be concise and direct. Do not say "I need to know your low stock threshold", just give the data you see.
        """

        if context == "dashboard":
            system_prompt += " The user is asking about business metrics."
        elif context == "order_summary":
            system_prompt += " Summarize the provided order details concisely."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000", 
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                content = data['choices'][0]['message']['content']
                return {"response": content}
            except Exception as e:
                print(f"AI Error: {e}")
                return {"response": "I'm having trouble connecting to my brain right now."}
