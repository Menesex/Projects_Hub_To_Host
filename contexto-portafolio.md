# Contexto de Arquitectura Definitivo: Projects Hub (Backend Unified)
**Developer:** Juan José Meneses Jaramillo
**Enfoque:** Monorrepósito optimizado para Hosting Gratuito (Render, 512MB RAM). Todo se unifica bajo un único proceso de Python (FastAPI) para compartir la misma memoria RAM y evitar la hibernación múltiple.

## 1. Estrategia de Integración Integrada (KISS Avanzado)
- **Frontends (React/Vite):** Se compilan con `npm run build`. El FastAPI del orquestador sirve la carpeta `dist/` resultante como archivos estáticos con `app.mount()` (0% impacto de RAM en servidor).
- **Backends (APIs):** Las rutas de backend de los proyectos (como las APIs de To-Do List o Employees Manager) se importan o se escriben directamente dentro del código del Orquestador usando `APIRouter` de FastAPI. Comparten el mismo ciclo de vida y la misma instancia de ejecución.
- **Base de Datos:** En desarrollo local se centraliza usando archivos SQLite independientes dentro de `orquestador/data/`. En producción, apuntarán a variables de entorno (.env).

## 2. Estructura Real y Limpia del Proyecto
MeneProjectPortfolio/
├── orquestador/                # El ÚNICO servidor vivo (FastAPI)
│   ├── main.py                 # Orquestador central + Rutas de APIs unificadas
│   ├── requirements.txt
│   ├── Procfile
│   ├── data/
│   │   ├── projects.json       # Configuración dinámica de las tarjetas
│   │   └── todo_list.db        # Base de datos SQLite local para el proyecto 1
│   ├── templates/
│   │   └── dashboard.html      # UI interactiva (Tailwind CSS)
│   └── static/
│       └── images/             # Screenshots o placeholders de respaldo
│
├── projects/
│   └── todo-list/              # Código fuente desacoplado del Proyecto 1
│       ├── frontend/           # Proyecto en React/Vite
│       │   └── dist/           # Carpeta compilada que lee el orquestador
│       └── backend/            # Lógica de Python/FastAPI copiada/referenciada al Hub
│
├── venv/                       # Único entorno virtual global
├── .env                        # Secretos y credenciales locales (Gitignored)
├── .env.example
└── README.md