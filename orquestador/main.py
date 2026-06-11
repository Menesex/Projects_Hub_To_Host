import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from apps.todo_list.router import router as todo_router
from apps.todo_list import models  # noqa: registers tables with Base

BASE_DIR = Path(__file__).resolve().parent
PARENT_DIR = BASE_DIR.parent

# DB inicializa lazy cuando se accede a una ruta que la necesita
# (en get_db() dependency)

app = FastAPI(title="Projects Hub")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo_router)

# Static files
if (BASE_DIR / "static").exists():
    app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

_todo_dist = PARENT_DIR / "projects" / "todo_list" / "frontend" / "dist"
if _todo_dist.exists():
    app.mount("/todo", StaticFiles(directory=str(_todo_dist), html=True), name="todo")

# Dashboard
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def load_projects():
    try:
        with open(BASE_DIR / "data" / "projects.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"developer": {}, "projects": []}

@app.get("/", response_class=HTMLResponse)
async def get_hub():
    data = load_projects()
    return templates.get_template("dashboard.html").render(
        developer=data.get("developer", {}),
        projects=data.get("projects", [])
    )

# Placeholder routes
@app.get("/api/employees", response_class=HTMLResponse)
async def get_employees():
    return HTMLResponse("<h1>Employees Manager - Próximamente</h1>")

@app.get("/graphix", response_class=HTMLResponse)
async def get_graphix():
    return HTMLResponse("<h1>PolyGraphiX - Próximamente</h1>")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
