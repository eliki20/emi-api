from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token

from app.projects.emi.domain.exceptions import EmailAlreadyExistsError, InvalidCredentialsError
from app.projects.emi.domain.models.user import UserCreate, UserInDB, UserLogin, UserPublic
from app.projects.emi.domain.security import create_access_token, hash_password, verify_password
from app.projects.emi.infra.repositories.user_repo import UserRepository
from app.projects.emi.infra.settings import settings


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register(self, data: UserCreate) -> tuple[UserPublic, str]:
        existing = await self.user_repo.get_by_email(data.correo)
        if existing:
            raise EmailAlreadyExistsError(f"El correo {data.correo} ya está registrado")

        user = UserInDB(
            nombre=data.nombre,
            correo=data.correo,
            password_hash=hash_password(data.password),
        )
        user_id = await self.user_repo.create(user)

        public = UserPublic(id=user_id, nombre=user.nombre, correo=user.correo)
        token = create_access_token(user_id, user.correo)
        return public, token

    async def login(self, data: UserLogin) -> tuple[UserPublic, str]:
        doc = await self.user_repo.get_by_email(data.correo)
        if not doc or not verify_password(data.password, doc["password_hash"]):
            raise InvalidCredentialsError("Correo o contraseña incorrectos")

        user_id = str(doc["_id"])
        public = UserPublic(id=user_id, nombre=doc["nombre"], correo=doc["correo"])
        token = create_access_token(user_id, doc["correo"])
        return public, token

    async def google_login(self, id_token_str: str) -> tuple[UserPublic, str]:
        try:
            idinfo = google_id_token.verify_oauth2_token(
                id_token_str, google_requests.Request(), settings.google_client_id
            )
        except ValueError:
            raise InvalidCredentialsError("Token de Google inválido")

        correo = idinfo["email"]
        nombre = idinfo.get("name", correo.split("@")[0])

        existing = await self.user_repo.get_by_email(correo)
        if existing:
            user_id = str(existing["_id"])
            public = UserPublic(id=user_id, nombre=existing["nombre"], correo=existing["correo"])
        else:
            user = UserInDB(nombre=nombre, correo=correo, password_hash="google_oauth_no_password")
            user_id = await self.user_repo.create(user)
            public = UserPublic(id=user_id, nombre=nombre, correo=correo)

        token = create_access_token(user_id, correo)
        return public, token