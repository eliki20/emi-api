import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv("credentials/emi.env")

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-3.5-flash")


async def generate_response(prompt: str) -> str:
    response = await model.generate_content_async(prompt)
    return response.text