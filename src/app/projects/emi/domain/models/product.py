from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    nombre: str
    categoria: str
    marca: str = ""
    precio: float
    stock: int = 0
    descripcion: str = ""
    imagen_url: str = ""


class ProductInDB(ProductCreate):
    id: str | None = None


class ProductPublic(BaseModel):
    id: str
    nombre: str
    categoria: str
    marca: str
    precio: float
    stock: int
    descripcion: str
    imagen_url: str
    disponible: bool = Field(default=True)