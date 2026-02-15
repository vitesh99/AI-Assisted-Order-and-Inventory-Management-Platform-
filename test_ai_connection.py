import asyncio
import logging
import sys

# Configure logging to show everything
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock settings loading to ensure we get what we expect
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("AI_API_KEY")
model = os.getenv("AI_MODEL", "google/gemini-2.0-flash-001")

print(f"--- AI Connection Test ---")
print(f"Key Length: {len(api_key) if api_key else 0}")
print(f"Model: {model}")

if not api_key:
    print("ERROR: No API Key found in .env")
    sys.exit(1)

from openai import AsyncOpenAI

async def test_generation():
    print("\nAttempting to connect to OpenRouter...")
    client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "https://ai-inventory-app", 
            "X-Title": "AI Inventory App"
        }
    )
    
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Say 'Hello from OpenRouter!'"}
            ],
        )
        print("\nSUCCESS! Response received:")
        print(response.choices[0].message.content)
    except Exception as e:
        print("\nFAILURE! Error details:")
        print(e)

if __name__ == "__main__":
    asyncio.run(test_generation())
