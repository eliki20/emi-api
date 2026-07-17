from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class ProductRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["productos"]

    async def list_all(self, categoria: str | None = None) -> list[dict]:
        query = {"categoria": categoria} if categoria else {}
        cursor = self.collection.find(query)
        return [doc async for doc in cursor]

    async def get_by_id(self, product_id: str) -> dict | None:
        if not ObjectId.is_valid(product_id):
            return None
        return await self.collection.find_one({"_id": ObjectId(product_id)})

    async def search(self, keyword: str) -> list[dict]:
        query = {
            "$or": [
                {"nombre": {"$regex": keyword, "$options": "i"}},
                {"descripcion": {"$regex": keyword, "$options": "i"}},
                {"categoria": {"$regex": keyword, "$options": "i"}},
            ]
        }
        cursor = self.collection.find(query)
        return [doc async for doc in cursor]

    async def create(self, product: dict) -> str:
        result = await self.collection.insert_one(product)
        return str(result.inserted_id)

    async def decrease_stock(self, product_id: str, cantidad: int) -> None:
        await self.collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$inc": {"stock": -cantidad}},
        )