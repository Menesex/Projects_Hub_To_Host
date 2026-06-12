# My To-Do List 📝

> A full-stack To-Do app inspired by Microsoft Outlook To-Do — built as a learning project from scratch.

# [🚀 CLICK TO LIVE DEMO!](https://my-yo-do-list-demo.vercel.app)

**|Live Demo:** [my-yo-do-list-demo.vercel.app](https://my-yo-do-list-demo.vercel.app) &nbsp;

|&nbsp; **API Docs:** [my-yo-do-list-demo.onrender.com/docs](https://my-yo-do-list-demo.onrender.com/docs)

---

## What it does

- Create, complete, and delete tasks
- Mark tasks as important ⭐
- Add sub-steps inside each task
- Set due dates and descriptions
- Filter tasks by **My Day**, **Important**, and **All Tasks**
- Changes persist in a real database — nothing is stored locally

---
---
![img](/images/img1.png)
---


## Tech Stack

### Frontend
| Technology | Purpose |
|---|---|
| React 19 + Vite | UI framework and dev server |
| Tailwind CSS v4 | Styling |
| Axios | HTTP requests to the API |
| lucide-react | Icons |
| Vercel | Hosting |

### Backend
| Technology | Purpose |
|---|---|
| FastAPI (Python) | REST API |
| SQLAlchemy | ORM / database access |
| Supabase (PostgreSQL) | Database |
| Pydantic | Data validation (schemas) |
| Render | Hosting |

---

## Architecture

```
┌─────────────────────┐        ┌──────────────────────────┐        ┌──────────────┐
│   React Frontend    │  HTTP  │     FastAPI Backend       │  SQL   │   Supabase   │
│   (Vercel)          │◄──────►│   (Render)                │◄──────►│  PostgreSQL  │
└─────────────────────┘        └──────────────────────────┘        └──────────────┘
```

---

## Project Structure

```
├── backend/
│   └── app/
│       ├── main.py        # App entry point, CORS config
│       ├── models.py      # Database tables (Task, Step)
│       ├── schemas.py     # Request/response shapes (Pydantic)
│       ├── crud.py        # Database operations
│       ├── database.py    # DB connection
│       └── routers/
│           └── tasks.py   # All API endpoints
│
└── frontend/
    └── src/
        ├── App.jsx              # Root component, global state
        ├── api.js               # All Axios API calls
        └── components/
            ├── Sidebar.jsx      # Left panel — category navigation
            ├── TaskList.jsx     # Middle panel — filtered task list
            ├── TaskItem.jsx     # Single task row (checkbox, star)
            └── TaskDetail.jsx   # Right panel — task editor + steps
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/tasks/` | Get all tasks (with nested steps) |
| `POST` | `/tasks/` | Create a task |
| `PATCH` | `/tasks/{id}` | Update a task |
| `DELETE` | `/tasks/{id}` | Delete a task |
| `POST` | `/tasks/{id}/steps` | Add a step to a task |
| `PATCH` | `/tasks/steps/{id}` | Toggle step completion |
| `DELETE` | `/tasks/steps/{id}` | Delete a step |

Full interactive docs: [my-yo-do-list-demo.onrender.com/docs](https://my-yo-do-list-demo.onrender.com/docs)

![img](/images/img2rutas.png)



## What I learned building this

- How to design and build a **REST API** with FastAPI from scratch
- How **Pydantic schemas** separate what the user sends from what the database stores
- How **SQLAlchemy ORM** maps Python classes to database tables
- How **CORS** works and why it matters for frontend/backend communication
- How to structure a **React app** with shared state across multiple components
- The difference between **pessimistic** and **optimistic UI updates** (and why it matters for UX)
- How to deploy a split frontend/backend project to **Vercel** and **Render**

---

## Roadmap - Features to add

- [ ] User authentication (login / signup)
- [ ] Multiple custom lists
- [ ] Drag to reorder tasks
- [ ] Mobile responsive layout
- [ ] Dark mode

![img](/images/features.png)
---

## Run it locally

### Backend
```bash
cd backend
pip install -r requirements.txt

# Create a .env file with your database URL:
# DATABASE_URL=postgresql+psycopg2://...

uvicorn app.main:app --reload
# Runs at http://localhost:8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# Runs at http://localhost:5173
```

> ⚠️ The frontend's `api.js` points to the production Render URL by default.
> Change `BASE_URL` to `http://localhost:8000` to use your local backend.

---
*Built with curiosity and a lot of Stack Overflow — [@Menesex](https://github.com/Menesex)*
