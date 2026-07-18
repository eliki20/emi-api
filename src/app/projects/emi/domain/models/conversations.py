from datetime import datetime, timezone

from pydantic import BaseModel, Field


class ChatMessageInDB(BaseModel):
    id: str | None = None
    usuario_id: str
    role: str  # "user" o "assistant"
    content: str
    creado_en: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ChatMessagePublic(BaseModel):
    id: str
    usuario_id: str
    role: str
    content: str
    creado_en: datetime