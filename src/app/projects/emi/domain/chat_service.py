from app.projects.emi.infra.clients.llm import generate_response
from app.projects.emi.infra.repositories.product_repo import ProductRepository
from app.projects.emi.infra.repositories.chat_repo import ChatRepository

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
    def __init__(self, product_repo: ProductRepository, chat_repo: ChatRepository):
        self.product_repo = product_repo
        self.chat_repo = chat_repo

    async def ask(self, usuario_id: str, pregunta: str) -> str:
        productos = await self.product_repo.search(pregunta)
        if not productos:
            productos = await self.product_repo.list_all()
        contexto = _build_context(productos)
        prompt_completo = f"""{SYSTEM_PROMPT}
        {contexto}
        Pregunta del cliente: {pregunta}
        Respuesta:"""
        respuesta = await generate_response(prompt_completo)
        await self.chat_repo.guardar_mensaje(usuario_id, pregunta, respuesta)
        return respuesta

    async def obtener_historial(self, usuario_id: str) -> list[dict]:
        return await self.chat_repo.obtener_historial(usuario_id)