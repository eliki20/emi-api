import asyncio
import sys
from pathlib import Path

# Permite importar "app..."
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from app.projects.emi.infra.db.mongo import get_database
from app.projects.emi.infra.clients.embedding import generate_embedding


async def main():
    db = get_database()
    collection = db["productos"]

    productos = await collection.find().to_list(length=None)

    print(f"\nSe encontraron {len(productos)} productos.\n")

    for i, producto in enumerate(productos, start=1):

        texto = f"""
Nombre: {producto.get("nombre","")}
Categoría: {producto.get("categoria","")}
Marca: {producto.get("marca","")}
Descripción: {producto.get("descripcion","")}
Precio: {producto.get("precio",0)}
        """

        print(f"[{i}/{len(productos)}] Generando embedding...")

        embedding = await generate_embedding(texto)

        await collection.update_one(
            {"_id": producto["_id"]},
            {
                "$set": {
                    "embedding": embedding
                }
            }
        )

        print(f"   ✓ {producto['nombre']}")

    print("\nTodos los embeddings fueron generados correctamente.")


if __name__ == "__main__":
    asyncio.run(main())