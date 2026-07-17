from datetime import datetime, timezone

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    nombre: str
    correo: EmailStr
    password: str


class UserLogin(BaseModel):
    correo: EmailStr
    password: str


class UserInDB(BaseModel):
    id: str | None = None
    nombre: str
    correo: EmailStr
    password_hash: str
    creado_en: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserPublic(BaseModel):
    id: str
    nombre: str
    correo: EmailStr