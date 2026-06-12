from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from sqlalchemy import create_engine, text
from contextlib import asynccontextmanager
from typing import Optional
from dotenv import load_dotenv
import os
import re

load_dotenv()

# --- DATABASE SETUP ---
# Locally: uses SQLite by default (no setup needed)
# Production: set DATABASE_URL env var to your PostgreSQL connection string
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./empleados.db")

# Render.com gives "postgres://" but SQLAlchemy needs "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

IS_POSTGRES = DATABASE_URL.startswith("postgresql")
engine = create_engine(DATABASE_URL)


def create_tables():
    # SERIAL = auto-increment in PostgreSQL, AUTOINCREMENT in SQLite
    id_col = "id SERIAL PRIMARY KEY" if IS_POSTGRES else "id INTEGER PRIMARY KEY AUTOINCREMENT"
    with engine.connect() as conn:
        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS employees (
                {id_col},
                name     TEXT    NOT NULL,
                access_id TEXT,
                area     TEXT    NOT NULL,
                position TEXT    NOT NULL,
                entry_hour TEXT  NOT NULL,
                active   BOOLEAN DEFAULT TRUE
            )
        """))
        conn.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield  # app runs here


# --- APP SETUP ---
app = FastAPI(title="Employee Management System", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for educational projects; restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_index():
    return FileResponse(os.path.join("templates", "index.html"))


# --- MODELS & VALIDATION ---
class Employee(BaseModel):
    id: Optional[int] = None
    name: str
    access_id: Optional[str] = None
    area: str
    position: str
    entry_hour: str
    active: bool = True

    @field_validator("name", "area", "position")
    @classmethod
    def validate_text(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Este campo no puede estar vacío")
        if len(v) > 100:
            raise ValueError("Máximo 100 caracteres")
        return v

    @field_validator("entry_hour")
    @classmethod
    def validate_time(cls, v: str) -> str:
        if not re.match(r"^\d{2}:\d{2}$", v):
            raise ValueError("Formato de hora inválido. Usa HH:MM")
        h, m = int(v[:2]), int(v[3:])
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError("Hora fuera de rango")
        return v

    @field_validator("access_id")
    @classmethod
    def validate_access_id(cls, v: Optional[str]) -> Optional[str]:
        if v:
            v = v.strip()
            if len(v) > 50:
                raise ValueError("Access ID: máximo 50 caracteres")
            return v or None
        return None


# --- ENDPOINTS ---

@app.get("/employees")
def get_employees(status: str = "all", search: str = "", search_type: str = "nombre"):
    # Whitelist columns to prevent SQL injection via search_type
    ALLOWED_COLUMNS = {"nombre": "name", "id": "id", "access_id": "access_id"}
    column = ALLOWED_COLUMNS.get(search_type, "name")

    try:
        with engine.connect() as conn:
            sql = "SELECT * FROM employees WHERE 1=1"
            params: dict = {}

            if status == "active":
                sql += " AND active = TRUE"
            elif status == "retired":
                sql += " AND active = FALSE"

            if search:
                sql += f" AND CAST({column} AS TEXT) LIKE :search"
                params["search"] = f"%{search}%"

            rows = conn.execute(text(sql), params).fetchall()
            return [dict(row._mapping) for row in rows]

    except Exception:
        raise HTTPException(status_code=500, detail="Error al obtener empleados")


@app.post("/employees", status_code=201)
def create_employee(emp: Employee):
    try:
        with engine.connect() as conn:
            params = {
                "name": emp.name,
                "access_id": emp.access_id,
                "area": emp.area,
                "position": emp.position,
                "entry_hour": emp.entry_hour,
            }

            if IS_POSTGRES:
                result = conn.execute(
                    text("INSERT INTO employees (name, access_id, area, position, entry_hour, active) "
                         "VALUES (:name, :access_id, :area, :position, :entry_hour, TRUE) RETURNING id"),
                    params,
                )
                new_id = result.scalar()
            else:
                result = conn.execute(
                    text("INSERT INTO employees (name, access_id, area, position, entry_hour, active) "
                         "VALUES (:name, :access_id, :area, :position, :entry_hour, 1)"),
                    params,
                )
                new_id = result.lastrowid

            conn.commit()
        return {"id": new_id}

    except Exception:
        raise HTTPException(status_code=500, detail="Error al crear el empleado")


@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, emp: Employee):
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("UPDATE employees SET name=:name, access_id=:access_id, area=:area, "
                     "position=:position, entry_hour=:entry_hour WHERE id=:id"),
                {
                    "name": emp.name,
                    "access_id": emp.access_id,
                    "area": emp.area,
                    "position": emp.position,
                    "entry_hour": emp.entry_hour,
                    "id": emp_id,
                },
            )
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Empleado no encontrado")
            conn.commit()
        return {"mensaje": "Actualizado"}

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error al actualizar el empleado")


@app.patch("/employees/{emp_id}/retire")
def retire_employee(emp_id: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("UPDATE employees SET active = FALSE, access_id = NULL WHERE id = :id"),
                {"id": emp_id},
            )
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Empleado no encontrado")
            conn.commit()
        return {"mensaje": "Retirado"}

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error al retirar el empleado")
