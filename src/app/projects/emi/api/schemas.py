from pydantic import BaseModel
from datetime import datetime

from app.projects.emi.domain.models.user import UserPublic


class AuthResponse(BaseModel):
    user: UserPublic
    access_token: str
    token_type: str = "bearer"


class ChatRequest(BaseModel):
    pregunta: str


class ChatResponse(BaseModel):
    respuesta: str


class GoogleLoginRequest(BaseModel):
    id_token: str


class DeviceTokenRequest(BaseModel):
    fcm_token: str

class MensajeHistorial(BaseModel):
    pregunta: str
    respuesta: str
    creado_en: datetime