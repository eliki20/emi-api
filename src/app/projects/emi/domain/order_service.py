from app.projects.emi.domain.exceptions import EmptyOrderError, StockInsuficienteError
from app.projects.emi.domain.models.order import OrderCreate, OrderInDB, OrderPublic
from app.projects.emi.infra.repositories.order_repo import OrderRepository
from app.projects.emi.infra.repositories.product_repo import ProductRepository


def _to_public(doc: dict) -> OrderPublic:
    return OrderPublic(
        id=str(doc["_id"]),
        usuario_id=doc["usuario_id"],
        items=doc["items"],
        total=doc["total"],
        estado=doc["estado"],
        creado_en=doc["creado_en"],
    )


class OrderService:
    def __init__(self, order_repo: OrderRepository, product_repo: ProductRepository):
        self.order_repo = order_repo
        self.product_repo = product_repo

    async def create_order(self, usuario_id: str, data: OrderCreate) -> OrderPublic:
        if not data.items:
            raise EmptyOrderError("El carrito está vacío")

        total = 0.0
        for item in data.items:
            product = await self.product_repo.get_by_id(item.producto_id)
            if not product or product.get("stock", 0) < item.cantidad:
                raise StockInsuficienteError(f"Stock insuficiente para {item.nombre}")
            total += product["precio"] * item.cantidad

        order = OrderInDB(usuario_id=usuario_id, items=data.items, total=total)
        order_id = await self.order_repo.create(order.model_dump(exclude={"id"}))

        for item in data.items:
            await self.product_repo.decrease_stock(item.producto_id, item.cantidad)

        doc = await self.order_repo.get_by_id(order_id)
        return _to_public(doc)

    async def list_user_orders(self, usuario_id: str) -> list[OrderPublic]:
        docs = await self.order_repo.list_by_user(usuario_id)
        return [_to_public(d) for d in docs]

    async def get_order(self, order_id: str) -> OrderPublic | None:
        doc = await self.order_repo.get_by_id(order_id)
        return _to_public(doc) if doc else None