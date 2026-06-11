import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from apps.todo_list.router import router as todo_router
from apps.todo_list import models  # noqa: registers tables with Base

# ==================== PATH RESOLUTION ====================
BASE_DIR = Path(__file__).resolve().parent  # orquestador/
PARENT_DIR = BASE_DIR.parent  # MeneProjectPortfolio/
PROJECTS_DIR = PARENT_DIR / "projects"

# Debug: Show directory structure
print("\n" + "="*70)
print("📂 DIRECTORY STRUCTURE")
print("="*70)
print(f"BASE_DIR (orquestador): {BASE_DIR}")
print(f"PARENT_DIR: {PARENT_DIR}")
print(f"PROJECTS_DIR: {PROJECTS_DIR}")
print("="*70 + "\n")

# ==================== FASTAPI APP ====================
app = FastAPI(title="Projects Hub")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo_router)

# ==================== STATIC FILES MOUNTING ====================

# Mount hub static files (CSS, JS, images)
hub_static = BASE_DIR / "static"
if hub_static.exists():
    print(f"✓ Mounting hub static: {hub_static}")
    app.mount("/static", StaticFiles(directory=str(hub_static)), name="static")
else:
    print(f"⚠ Hub static not found: {hub_static}")

# Mount To-Do List frontend (compiled dist/)
todo_dist = PROJECTS_DIR / "todo_list" / "frontend" / "dist"
if todo_dist.exists():
    print(f"✓ Mounting To-Do List: {todo_dist}")
    app.mount("/todo", StaticFiles(directory=str(todo_dist), html=True), name="todo")
else:
    print(f"⚠ To-Do List dist not found: {todo_dist}")
    print(f"  Expected at: {todo_dist}")

print()

# ==================== TEMPLATES ====================
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def load_projects():
    try:
        with open(BASE_DIR / "data" / "projects.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"developer": {}, "projects": []}


# ==================== ROUTES ====================

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
