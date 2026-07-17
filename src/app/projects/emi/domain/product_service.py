from app.projects.emi.domain.models.product import ProductPublic
from app.projects.emi.infra.repositories.product_repo import ProductRepository


def _to_public(doc: dict) -> ProductPublic:
    return ProductPublic(
        id=str(doc["_id"]),
        nombre=doc["nombre"],
        categoria=doc["categoria"],
        marca=doc.get("marca", ""),
        precio=doc["precio"],
        stock=doc.get("stock", 0),
        descripcion=doc.get("descripcion", ""),
        imagen_url=doc.get("imagen_url", ""),
        disponible=doc.get("stock", 0) > 0,
    )

class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def list_products(self, categoria: str | None = None) -> list[ProductPublic]:
        docs = await self.repo.list_all(categoria)
        return [_to_public(d) for d in docs]

    async def get_product(self, product_id: str) -> ProductPublic | None:
        doc = await self.repo.get_by_id(product_id)
        return _to_public(doc) if doc else None

    async def search_products(self, keyword: str) -> list[ProductPublic]:
        docs = await self.repo.search(keyword)
        return [_to_public(d) for d in docs]