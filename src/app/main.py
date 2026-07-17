from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.core.discovery import load_projects, registry

app = FastAPI(title="EMI API", version="1.0.0")

print("STARTING APP")
load_projects(app)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def landing():
    cards = ""
    for project in registry:
        route_rows = "".join(
            f'<tr><td>{r.split()[0]}</td><td>{project["prefix"]}{r.split(" ", 1)[1]}</td></tr>'
            for r in project["routes"]
        )
        cards += f"""
        <div>
            <h2>{project["name"]}</h2>
            <a href="{project["prefix"]}/health">health</a> |
            <a href="/docs">docs</a>
            <table>{route_rows}</table>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><title>EMI API</title></head>
<body>
  <h1>EMI API</h1>
  <p>{len(registry)} proyecto(s), {sum(len(p["routes"]) for p in registry)} endpoint(s)</p>
  {cards}
</body>
</html>"""