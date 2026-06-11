# 🚀 Deployment to Render

This document explains how to deploy the Projects Hub to Render while maintaining the full project structure.

## Project Structure (No Moving Required)

```
MeneProjectPortfolio/
├── orquestador/              ← FastAPI application lives here
│   ├── main.py              ← Entry point (finds dist via ../projects/)
│   ├── database.py
│   ├── requirements.txt
│   ├── apps/
│   │   └── todo_list/
│   ├── templates/
│   └── data/
│
└── projects/                ← Frontend source code lives here
    └── todo_list/
        └── frontend/
            └── dist/        ← Compiled assets (NOT duplicated)
```

## Why This Structure?

- **No duplication**: `dist/` stays in its original location
- **Single source of truth**: Frontend builds once, served from one place
- **Easy updates**: Run `npm run build` in `projects/todo_list/frontend/`, and it's instantly available
- **Render compatibility**: Works because we `cd orquestador` before running the app

## Render Configuration

### 1. Create New Web Service

Go to https://dashboard.render.com and create a **New** → **Web Service**

### 2. Connect Repository

- **Repository**: `https://github.com/Menesex/Projects_Hub_To_Host.git`
- **Branch**: `main`

### 3. Configure Service Settings

**Name**: `projects-hub` (or your preferred name)

**Root Directory**: `.` (empty or dot) — **IMPORTANT: NOT `orquestador/`**

This allows Render to access both `orquestador/` and `projects/` directories.

### 4. Build & Start Commands

**Build Command**:
```bash
cd orquestador && pip install -r requirements.txt
```

**Start Command**:
```bash
cd orquestador && uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 5. Environment Variables

In Render dashboard → **Environment** section, add:

```
DATABASE_URL=postgresql://postgres.YOUR_USER:YOUR_PASSWORD@YOUR_HOST:6543/postgres
```

Get this from Supabase → Settings → Database → Connection pooler → URI

### 6. Deploy

Click **Create Web Service** and Render will:
1. Clone your repo
2. Run build command (installs dependencies in orquestador/)
3. Run start command (boots FastAPI from orquestador/, finds dist/ via ../projects/)

---

## How Path Resolution Works

In `main.py`:
```python
BASE_DIR = Path(__file__).resolve().parent  # = orquestador/
PARENT_DIR = BASE_DIR.parent                 # = MeneProjectPortfolio/
todo_dist = PARENT_DIR / "projects" / "todo_list" / "frontend" / "dist"
```

This works **both locally and on Render** because:
- Locally: `uvicorn main:app` from `orquestador/` → finds `../projects/` ✓
- Render: `cd orquestador && uvicorn main:app` → finds `../projects/` ✓

---

## Testing Before Deploy

```bash
# Locally, from the root:
cd orquestador
uvicorn main:app --reload
```

Visit http://localhost:8000/todo — should work immediately if `dist/` exists.

If you see `⚠ To-Do List dist not found`, run:
```bash
cd projects/todo_list/frontend
npm run build
```

---

## Scaling to More Projects

Once deployed, to add Employees Manager:

1. Create `orquestador/apps/employees/` with same structure as `todo_list/`
2. Build frontend: `cd projects/employees_manager/frontend && npm run build`
3. Add to `main.py`:
   ```python
   from apps.employees.router import router as employees_router
   app.include_router(employees_router)
   ```
4. Add to `orquestador/data/projects.json`:
   ```json
   {
     "id": "employees-manager",
     "name": "Employees Manager",
     "url": "/api/employees/tasks",
     ...
   }
   ```
5. Commit & push — Render redeploys automatically

---

## Troubleshooting

**"dist not found"**: Run `npm run build` in the frontend folder locally, commit, push.

**"Database connection failed"**: Check DATABASE_URL in Render environment variables.

**"404 on /todo"**: Ensure `projects/todo_list/frontend/dist/` has `index.html`.

---

✨ You're deploying a production-grade, scalable hub with minimal complexity!
