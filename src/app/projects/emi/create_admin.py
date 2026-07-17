import asyncio

from app.projects.emi.infra.db.mongo import get_database
from app.projects.emi.domain.security import hash_password


async def main():
    db = get_database()
    correo = "admin@emi.com"
    password = "admin123"

    existing = await db["usuarios"].find_one({"correo": correo})
    if existing:
        await db["usuarios"].update_one({"correo": correo}, {"$set": {"rol": "admin"}})
        print(f"✅ Usuario {correo} actualizado a rol admin")
    else:
        await db["usuarios"].insert_one({
            "nombre": "Administrador EMI",
            "correo": correo,
            "password_hash": hash_password(password),
            "rol": "admin",
        })
        print(f"✅ Usuario admin creado: {correo} / {password}")


asyncio.run(main())