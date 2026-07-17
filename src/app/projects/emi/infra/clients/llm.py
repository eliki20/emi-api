from google import genai

from app.projects.emi.infra.settings import settings

client = genai.Client(api_key=settings.gemini_api_key)


async def generate_response(prompt: str) -> str:
    response = await client.aio.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )
    return response.text