from fastapi import APIRouter, Depends, HTTPException, status

from app.projects.emi.api.deps import get_auth_service
from app.projects.emi.api.schemas import AuthResponse
from app.projects.emi.domain.auth_service import AuthService
from app.projects.emi.domain.exceptions import EmailAlreadyExistsError, InvalidCredentialsError
from app.projects.emi.domain.models.user import UserCreate, UserLogin
from app.projects.emi.api.deps import get_product_service
from app.projects.emi.domain.product_service import ProductService
from app.projects.emi.domain.models.product import ProductPublic
from app.projects.emi.api.auth import get_current_user_id
from app.projects.emi.api.deps import get_order_service
from app.projects.emi.domain.order_service import OrderService
from app.projects.emi.domain.exceptions import EmptyOrderError, StockInsuficienteError
from app.projects.emi.domain.models.order import OrderCreate, OrderPublic
from app.projects.emi.api.deps import get_chat_service
from app.projects.emi.domain.chat_service import ChatService
from app.projects.emi.api.schemas import ChatRequest, ChatResponse
from app.projects.emi.api.schemas import GoogleLoginRequest

router = APIRouter(tags=["emi"])


@router.get("/health")
async def health():
    return {"status": "ok", "project": "emi"}


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, auth: AuthService = Depends(get_auth_service)):
    try:
        user, token = await auth.register(data)
    except EmailAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return AuthResponse(user=user, access_token=token)


@router.post("/login", response_model=AuthResponse)
async def login(data: UserLogin, auth: AuthService = Depends(get_auth_service)):
    try:
        user, token = await auth.login(data)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return AuthResponse(user=user, access_token=token)

@router.get("/productos", response_model=list[ProductPublic])
async def listar_productos(
    categoria: str | None = None,
    products: ProductService = Depends(get_product_service),
):
    return await products.list_products(categoria)


@router.get("/productos/buscar", response_model=list[ProductPublic])
async def buscar_productos(
    q: str,
    products: ProductService = Depends(get_product_service),
):
    return await products.search_products(q)


@router.get("/productos/{product_id}", response_model=ProductPublic)
async def obtener_producto(
    product_id: str,
    products: ProductService = Depends(get_product_service),
):
    product = await products.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.post("/pedidos", response_model=OrderPublic, status_code=status.HTTP_201_CREATED)
async def crear_pedido(
    data: OrderCreate,
    usuario_id: str = Depends(get_current_user_id),
    orders: OrderService = Depends(get_order_service),
):
    try:
        return await orders.create_order(usuario_id, data)
    except EmptyOrderError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except StockInsuficienteError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/pedidos", response_model=list[OrderPublic])
async def listar_mis_pedidos(
    usuario_id: str = Depends(get_current_user_id),
    orders: OrderService = Depends(get_order_service),
):
    return await orders.list_user_orders(usuario_id)


@router.get("/pedidos/{order_id}", response_model=OrderPublic)
async def obtener_pedido(
    order_id: str,
    orders: OrderService = Depends(get_order_service),
):
    order = await orders.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return order

@router.post("/chat", response_model=ChatResponse)
async def chat(
    data: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
):
    respuesta = await chat_service.ask(data.pregunta)
    return ChatResponse(respuesta=respuesta)

@router.post("/google-login", response_model=AuthResponse)
async def google_login(data: GoogleLoginRequest, auth: AuthService = Depends(get_auth_service)):
    try:
        user, token = await auth.google_login(data.id_token)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return AuthResponse(user=user, access_token=token)