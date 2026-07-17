from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class OrderRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["pedidos"]

    async def create(self, order: dict) -> str:
        result = await self.collection.insert_one(order)
        return str(result.inserted_id)

    async def list_by_user(self, usuario_id: str) -> list[dict]:
        cursor = self.collection.find({"usuario_id": usuario_id}).sort("creado_en", -1)
        return [doc async for doc in cursor]

    async def get_by_id(self, order_id: str) -> dict | None:
        if not ObjectId.is_valid(order_id):
            return None
        return await self.collection.find_one({"_id": ObjectId(order_id)})
    
    async def update_status(self, order_id: str, nuevo_estado: str) -> None:
        await self.collection.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"estado": nuevo_estado}},
        )

        