from openai import AsyncOpenAI
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class AIClient:
    def __init__(self):
        self.api_key = settings.AI_API_KEY
        self.model_name = settings.AI_MODEL
        self.enabled = settings.ENABLE_AI
        self.client = None
        
        if self.enabled:
            if self.api_key:
                try:
                    # OpenRouter Configuration
                    self.client = AsyncOpenAI(
                        api_key=self.api_key,
                        base_url="https://openrouter.ai/api/v1",
                        default_headers={
                            "HTTP-Referer": "https://ai-inventory-app", # Required by OpenRouter
                            "X-Title": "AI Inventory App"
                        }
                    )
                    logger.info(f"AI Client initialized with OpenRouter model {self.model_name}")
                except Exception as e:
                    logger.error(f"Failed to configure AI client: {e}")
            else:
                logger.warning("AI enabled but no API Key provided in settings.")

    async def generate_text(self, prompt: str) -> str | None:
        if not self.enabled or not self.client:
            return None
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )
            
            if response.choices and response.choices[0].message.content:
                return response.choices[0].message.content
            return None
        except Exception as e:
            logger.error(f"AI Generation failed: {e}")
            return None

ai_client = AIClient()
