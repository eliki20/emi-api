import asyncio
from typing import Optional

import firebase_admin
from firebase_admin import credentials, messaging

from app.projects.emi.infra.settings import ENV_PATH

_cred_path = ENV_PATH.parent / "emi-firebase-adminsdk.json"  # confírmame el nombre exacto
_app = firebase_admin.initialize_app(credentials.Certificate(str(_cred_path)), name="emi")


async def send_push(
    fcm_token: str,
    title: str,
    body: str,
    data: Optional[dict[str, str]] = None,
) -> str | None:
    message = messaging.Message(
        token=fcm_token,
        notification=messaging.Notification(title=title, body=body),
        data=data or {},
    )
    try:
        return await asyncio.to_thread(messaging.send, message, app=_app)
    except Exception as e:
        # Token inválido/expirado (dispositivo desinstaló la app, token rotó, etc.)
        print(f"Error enviando push FCM: {e}")
        return None