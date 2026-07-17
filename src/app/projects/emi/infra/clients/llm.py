import os
import google.generativeai as genai


genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-1.5-flash")


async def generate_response(prompt: str) -> str:
    response = await model.generate_content_async(prompt)

    return response.text.strip()