import asyncio

from google import genai
from google.genai.errors import APIError

from app.projects.emi.infra.settings import settings

client = genai.Client(api_key=settings.gemini_api_key)


async def generate_response(prompt: str) -> str:

    MAX_INTENTOS = 3

    for intento in range(MAX_INTENTOS):

        try:
            print(f"Modelo usado: {settings.gemini_model}")

            response = await client.aio.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
            )

            return response.text or "No pude generar una respuesta."

        except APIError as e:

            print("===== GEMINI API ERROR =====")
            print(e)
            print("============================")

            # Obtenemos el código si existe
            codigo = getattr(e, "code", None)

            if codigo == 429:
                if intento < MAX_INTENTOS - 1:
                    print("Esperando 45 segundos para reintentar...")
                    await asyncio.sleep(45)
                    continue

                return (
                    "Se alcanzó el límite gratuito de la IA. "
                    "Intenta nuevamente en aproximadamente un minuto."
                )

            if codigo == 503:
                if intento < MAX_INTENTOS - 1:
                    await asyncio.sleep(2)
                    continue

                return (
                    "La IA está temporalmente ocupada. "
                    "Intenta nuevamente en unos segundos."
                )

            return "No fue posible generar una respuesta."

        except Exception as e:

            print("===== ERROR GENERAL =====")
            print(e)
            print("=========================")

            return (
                "Ocurrió un problema al comunicarse con la IA."
            )