from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.projects.emi.domain.models.user import UserInDB


class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["usuarios"]

    async def get_by_email(self, correo: str) -> dict | None:
        return await self.collection.find_one({"correo": correo})

    async def get_by_id(self, user_id: str) -> dict | None:
        if not ObjectId.is_valid(user_id):
            return None
        return await self.collection.find_one({"_id": ObjectId(user_id)})

    async def create(self, user: UserInDB) -> str:
        doc = user.model_dump(exclude={"id"})
        result = await self.collection.insert_one(doc)
        return str(result.inserted_id)