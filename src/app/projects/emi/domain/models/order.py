from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    PENDIENTE = "Pendiente"
    EN_PREPARACION = "En preparación"
    LISTO = "Listo para entrega"
    ENTREGADO = "Entregado"


class OrderItem(BaseModel):
    producto_id: str
    nombre: str
    cantidad: int
    precio_unitario: float


class OrderCreate(BaseModel):
    items: list[OrderItem]


class OrderInDB(BaseModel):
    id: str | None = None
    usuario_id: str
    items: list[OrderItem]
    total: float
    estado: OrderStatus = OrderStatus.PENDIENTE
    creado_en: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class OrderPublic(BaseModel):
    id: str
    usuario_id: str
    items: list[OrderItem]
    total: float
    estado: OrderStatus
    creado_en: datetime