from app.projects.emi.infra.clients.llm import generate_response
from app.projects.emi.infra.repositories.product_repo import ProductRepository

SYSTEM_PROMPT = """Eres el asistente virtual de EMI, una librería de útiles escolares.

TU ÚNICO PROPÓSITO es ayudar a los clientes a elegir útiles escolares según:
- El grado o nivel escolar de sus hijos
- Su presupuesto disponible
- El tipo de actividad (dibujo, matemática, manualidades, etc.)

REGLAS ESTRICTAS:
1. SOLO puedes recomendar productos de la lista de "PRODUCTOS DISPONIBLES" que se te entrega abajo.
2. Nunca inventes productos que no estén en esa lista.
3. Si el cliente pregunta algo que NO tiene relación con útiles escolares o la librería
   (por ejemplo: programación, tareas de otras materias, temas personales, noticias, etc.),
   responde amablemente que solo puedes ayudar con temas de la librería EMI y útiles escolares,
   y no respondas la pregunta fuera de tema.
4. Sé breve, cálido y directo. Responde en español.
5. Si mencionas precios, usa el formato "S/" (soles).
"""


def _build_context(productos: list[dict]) -> str:
    if not productos:
        return "PRODUCTOS DISPONIBLES: (no se encontraron productos relacionados en este momento)"

    lineas = ["PRODUCTOS DISPONIBLES:"]
    for p in productos:
        lineas.append(
            f"- {p['nombre']} | Categoría: {p['categoria']} | Precio: S/{p['precio']} | Stock: {p.get('stock', 0)}"
        )
    return "\n".join(lineas)


class ChatService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def ask(self, pregunta: str) -> str:
        # Busca productos relevantes usando la misma búsqueda por texto que ya tienes
        productos = await self.product_repo.search(pregunta)

        # Si la búsqueda por palabra clave no encuentra nada, manda el catálogo completo
        # (para preguntas generales como "qué necesito para segundo grado")
        if not productos:
            productos = await self.product_repo.list_all()

        contexto = _build_context(productos)

        prompt_completo = f"""{SYSTEM_PROMPT}

        {contexto}

        Pregunta del cliente: {pregunta}

        Respuesta:"""

        return await generate_response(prompt_completo)