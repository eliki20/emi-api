import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"


async def generate_response(prompt: str) -> str:
    async with httpx.AsyncClient(timeout=90.0) as client:
        response = await client.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()