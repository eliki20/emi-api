from motor.motor_asyncio import AsyncIOMotorDatabase


class DeviceTokenRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["device_tokens"]

    async def upsert(self, usuario_id: str, fcm_token: str) -> None:
        await self.collection.update_one(
            {"usuario_id": usuario_id},
            {"$set": {"fcm_token": fcm_token}},
            upsert=True,
        )

    async def get_token(self, usuario_id: str) -> str | None:
        doc = await self.collection.find_one({"usuario_id": usuario_id})
        return doc["fcm_token"] if doc else None