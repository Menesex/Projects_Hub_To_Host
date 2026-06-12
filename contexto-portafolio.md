# Contexto del Proyecto: Multi-App Portfolio Hub

## 🌌 Estado Actual del Sistema
- **Arquitectura:** Monorepo orquestador basado en FastAPI (Backend unificado) que sirve múltiples aplicaciones de Frontend estáticas (compiladas en `dist/` con Vite).
- **Base de Datos:** PostgreSQL en Supabase en producción (funcionando al 100% con la contraseña e hilos de conexión activos). SQLite para desarrollo local (`app.db`).
- **Despliegue:** Hosteado exitosamente en Render como un único Web Service dinámico.
  - Root Directory: `.` (Raíz)
  - Build Command: `cd orquestador && pip install -r requirements.txt`
  - Start Command: `cd orquestador && uvicorn main:app --host 0.0.0.0 --port $PORT`

## 📂 Estructura del Repositorio Real
MeneProjectPortfolio/
├── orquestador/              ← Aplicación FastAPI central (Lobby)
│   ├── main.py              ← Punto de entrada (Router central y montajes)
│   ├── database.py          ← Configuración de SQLAlchemy con variables de entorno
│   ├── requirements.txt     
│   ├── apps/
│   │   └── todo_list/       ← Backend modular de la App 1 (Modelos, routers, crud)
│   ├── static/              ← Assets estáticos del lobby
│   └── templates/           ← dashboard.html (El home del portafolio)
└── projects/
    └── todo_list/
        └── frontend/
            └── dist/        ← Código React compilado de la App 1

## 🚀 Nueva Misión: Integrar "Employees Manager"
Queremos clonar e integrar el segundo proyecto al ecosistema sin romper la estructura modular establecida.

### Repositorio a clonar:
`https://github.com/Menesex/Employees_manager`

### Objetivo final de carpetas:
- Clonar el repositorio en: `projects/employees_manager/`
- Crear el módulo de backend en: `orquestador/apps/employees/` (replicando la lógica de models, schemas, crud y router de la nueva app).
- Compilar el frontend de empleados e integrarlo en `main.py` mediante un nuevo montaje estático (`app.mount("/employees", ...)`).
- Actualizar `orquestador/data/projects.json` para que el proyecto aparezca dinámicamente en el Lobby principal.