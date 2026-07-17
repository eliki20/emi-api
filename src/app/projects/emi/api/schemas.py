from pydantic import BaseModel

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