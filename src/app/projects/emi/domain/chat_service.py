import asyncio
import re

from app.projects.emi.infra.clients.embedding import generate_embedding
from app.projects.emi.infra.clients.llm import generate_response
from app.projects.emi.infra.repositories.chat_repo import ChatRepository
from app.projects.emi.infra.repositories.product_repo import ProductRepository

SYSTEM_PROMPT = """
Eres el asistente virtual de EMI, una librería de útiles escolares.

TU ÚNICO PROPÓSITO es ayudar a los clientes a elegir útiles escolares.

REGLAS:

1. SOLO puedes recomendar productos que aparezcan en PRODUCTOS DISPONIBLES.
2. Nunca inventes productos.
3. La CONVERSACIÓN RECIENTE es el contexto principal.
4. Si el usuario dice cosas como:
   - otro
   - otra
   - también
   - con S/40
   - con más presupuesto
   - ese
   - ellos
   - esos
   debes asumir que continúa la conversación anterior.
5. Solo cambia completamente de contexto si el usuario hace una nueva consulta claramente distinta.
6. Si la pregunta actual inicia un tema nuevo, ignora completamente la conversación anterior.
7. Si la pregunta continúa una conversación previa, utiliza únicamente la información relevante de esa conversación.
8. No saludes nuevamente en cada respuesta.
9. Responde de manera natural.
10. Si pregunta algo fuera de la librería, indícalo amablemente y no respondas ese punto.
11. Sé breve.
12. Usa S/ para los precios.
"""


def _build_context(productos: list[dict]) -> str:
    if not productos:
        return "PRODUCTOS DISPONIBLES: (No se encontraron productos.)"
    lineas = ["PRODUCTOS DISPONIBLES:"]
    for p in productos:
        lineas.append(
            f"- {p['nombre']} (marca {p.get('marca', 'genérica')}) | "
            f"Categoría: {p['categoria']} | "
            f"Precio: S/{p['precio']} | Stock: {p.get('stock', 0)}"
        )
    return "\n".join(lineas)


def _es_nueva_consulta(pregunta: str) -> bool:
    pregunta = pregunta.lower().strip()
    inicios = ("necesito", "quiero", "busco", "requiero", "deseo")
    continuacion = (
        "otro", "otra", "también", "tambien", "más", "mas", "ese", "esa",
        "ellos", "ellas", "con ", "entonces", "y si",
    )
    if pregunta.startswith(continuacion):
        return False
    if pregunta.startswith(inicios):
        return True
    return False


def _extraer_presupuesto(texto: str):
    m = re.search(r"(\d+)", texto)
    return m.group(1) if m else None


def _extraer_grado(texto: str):
    texto = texto.lower()
    for grado in ["inicial", "primaria", "secundaria"]:
        if grado in texto:
            return grado
    return None


def _extraer_actividad(texto: str):
    texto = texto.lower()
    actividades = ["matemática", "matematica", "geometría", "geometria",
                   "dibujo", "arte", "manualidades", "escritura"]
    for actividad in actividades:
        if actividad in texto:
            return actividad
    return None


def _build_history(historial: list[dict]) -> str:
    if not historial:
        return ""
    texto = "CONVERSACIÓN RECIENTE:\n"
    for m in historial:
        texto += f"Usuario: {m['pregunta']}\n"
        texto += f"Asistente: {m['respuesta']}\n"
    return texto


class ChatService:
    def __init__(self, product_repo: ProductRepository, chat_repo: ChatRepository):
        self.product_repo = product_repo
        self.chat_repo = chat_repo

    def _respuesta_rapida(self, pregunta: str) -> str | None:
        pregunta = pregunta.lower().strip()
        if pregunta in {"hola", "holi", "hello", "buenas", "buenos dias",
                         "buenos días", "buenas tardes", "buenas noches"}:
            return ("¡Hola! 👋 Soy EMI, el asistente virtual de la librería EMI. "
                     "Puedo ayudarte a encontrar útiles escolares según el grado escolar, "
                     "tu presupuesto o la actividad que necesites.")
        if pregunta in {"gracias", "muchas gracias", "gracias emi"}:
            return "¡Con mucho gusto! 😊"
        if pregunta in {"adios", "adiós", "chau", "chao", "hasta luego", "nos vemos"}:
            return "¡Hasta luego! 👋"
        return None

    async def ask(self, usuario_id: str, pregunta: str) -> str:
        respuesta = self._respuesta_rapida(pregunta)
        if respuesta:
            await self.chat_repo.guardar_mensaje(usuario_id, pregunta, respuesta)
            return respuesta

        es_nueva = _es_nueva_consulta(pregunta)

        historial, embedding_base = await asyncio.gather(
            self.chat_repo.obtener_historial(usuario_id, limite=5),
            generate_embedding(pregunta),
        )

        consulta_busqueda = pregunta
        necesita_reembeber = False

        if not es_nueva and historial:
            ultima = historial[-1]["pregunta"]
            presupuesto = _extraer_presupuesto(pregunta)
            if presupuesto:
                consulta_busqueda += f" presupuesto {presupuesto}"
                necesita_reembeber = True
            grado = _extraer_grado(ultima)
            if grado:
                consulta_busqueda += f" {grado}"
                necesita_reembeber = True
            actividad = _extraer_actividad(ultima)
            if actividad:
                consulta_busqueda += f" {actividad}"
                necesita_reembeber = True

        if necesita_reembeber:
            embedding_final = await generate_embedding(consulta_busqueda)
        else:
            embedding_final = embedding_base

        productos = await self.product_repo.search_by_embedding(embedding_final)

        productos_unicos, vistos = [], set()
        for p in productos:
            clave = (p["nombre"], p.get("marca", ""))
            if clave not in vistos:
                productos_unicos.append(p)
                vistos.add(clave)
        productos = productos_unicos

        if not productos:
            productos = await self.product_repo.list_all()

        contexto = _build_context(productos)
        historial_texto = _build_history(historial)

        prompt = f"""{SYSTEM_PROMPT}

{historial_texto}

{contexto}

Pregunta actual:
{pregunta}

Respuesta:
"""

        respuesta = await generate_response(prompt)
        await self.chat_repo.guardar_mensaje(usuario_id, pregunta, respuesta)
        return respuesta

    async def obtener_historial(self, usuario_id: str) -> list[dict]:
        return await self.chat_repo.obtener_historial(usuario_id)