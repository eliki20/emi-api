from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorDatabase


class ChatRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["chat_historial"]

    async def guardar_mensaje(self, usuario_id: str, pregunta: str, respuesta: str) -> None:
        await self.collection.insert_one({
            "usuario_id": usuario_id,
            "pregunta": pregunta,
            "respuesta": respuesta,
            "creado_en": datetime.now(timezone.utc),
        })

    async def obtener_historial(self, usuario_id: str, limite: int = 20) -> list[dict]:
        cursor = (
            self.collection.find({"usuario_id": usuario_id})
            .sort("creado_en", -1)
            .limit(limite)
        )
        mensajes = await cursor.to_list(length=limite)
        mensajes.reverse()
        return mensajes