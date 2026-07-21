from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.projects.emi.infra.clients.embedding import generate_embedding


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

    async def search_by_embedding(self, embedding: list[float]) -> list[dict]:
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": embedding,
                    "numCandidates": 50,
                    "limit": 5
                }
            },
            {
                "$project": {
                    "nombre": 1,
                    "categoria": 1,
                    "marca": 1,
                    "descripcion": 1,
                    "precio": 1,
                    "stock": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]
        cursor = self.collection.aggregate(pipeline)
        return [doc async for doc in cursor]

    async def create(self, product: dict) -> str:
        result = await self.collection.insert_one(product)
        return str(result.inserted_id)

    async def decrease_stock(self, product_id: str, cantidad: int) -> None:
        await self.collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$inc": {"stock": -cantidad}},
        )