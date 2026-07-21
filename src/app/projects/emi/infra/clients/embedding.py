import asyncio

from google import genai
from google.genai.errors import APIError

from app.projects.emi.infra.settings import settings

client = genai.Client(api_key=settings.gemini_api_key)


async def generate_embedding(text: str) -> list[float]:
    MAX_INTENTOS = 3

    for intento in range(MAX_INTENTOS):
        try:
            response = await client.aio.models.embed_content(
                model="gemini-embedding-001",
                contents=text,
            )
            return response.embeddings[0].values

        except APIError as e:
            print("===== GEMINI EMBEDDING ERROR =====")
            print(e)
            print("===================================")

            codigo = getattr(e, "code", None)

            if codigo == 429:
                if intento < MAX_INTENTOS - 1:
                    print("Límite de embeddings alcanzado, esperando 45 segundos...")
                    await asyncio.sleep(45)
                    continue
                raise

            if codigo == 503:
                if intento < MAX_INTENTOS - 1:
                    await asyncio.sleep(2)
                    continue
                raise

            raise