from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
from pathlib import Path

app = FastAPI(title="Projects Hub")

BASE_DIR = Path(__file__).resolve().parent
PARENT_DIR = BASE_DIR.parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

if (BASE_DIR / "static").exists():
    app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

if (PARENT_DIR / "1-todo-list").exists():
    app.mount("/todo", StaticFiles(directory=str(PARENT_DIR / "1-todo-list"), html=True), name="todo")


def load_projects():
    projects_file = BASE_DIR / "data" / "projects.json"
    try:
        with open(projects_file, "r", encoding="utf-8") as f:
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


@app.get("/api/employees", response_class=HTMLResponse)
async def get_employees():
    return HTMLResponse("<h1>Employees Manager - Próximamente</h1>")


@app.get("/graphix", response_class=HTMLResponse)
async def get_graphix():
    return HTMLResponse("<h1>PolyGraphiX - Próximamente</h1>")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)