from motor.motor_asyncio import AsyncIOMotorDatabase

from app.projects.emi.infra.db.mongo import get_database
from app.projects.emi.infra.repositories.user_repo import UserRepository
from app.projects.emi.domain.auth_service import AuthService
from app.projects.emi.infra.repositories.product_repo import ProductRepository
from app.projects.emi.domain.product_service import ProductService
from app.projects.emi.infra.repositories.order_repo import OrderRepository
from app.projects.emi.domain.order_service import OrderService
from app.projects.emi.domain.chat_service import ChatService
from app.projects.emi.infra.repositories.device_token_repo import DeviceTokenRepository
from app.projects.emi.infra.repositories.chat_repo import ChatRepository

def get_db() -> AsyncIOMotorDatabase:
    return get_database()


def get_auth_service() -> AuthService:
    db = get_db()
    return AuthService(UserRepository(db))


def get_product_service() -> ProductService:
    db = get_db()
    return ProductService(ProductRepository(db))

def get_order_service() -> OrderService:
    db = get_db()
    return OrderService(OrderRepository(db), ProductRepository(db), DeviceTokenRepository(db))

def get_chat_service() -> ChatService:
    db = get_db()
    return ChatService(ProductRepository(db))

def get_device_token_repo() -> DeviceTokenRepository:
    db = get_db()
    return DeviceTokenRepository(db)

def get_chat_service() -> ChatService:
    db = get_db()
    return ChatService(ProductRepository(db), ChatRepository(db))