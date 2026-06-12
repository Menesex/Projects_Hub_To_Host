# 🚀 Setup & Development Guide

## Local Development Setup

### 1. Prerequisites
- Python 3.10+
- Node.js 18+
- Git
- Groq API Key (for Plant Detect feature)

### 2. Clone & Install

```bash
# Clone repository
git clone https://github.com/Menesex/Projects_Hub_To_Host.git
cd Projects_Hub_To_Host

# Create Python virtual environment
cd orquestador
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your values
nano .env
```

Required environment variables:
- `GROQ_API_KEY` - Get from https://console.groq.com/keys
- `DATABASE_URL` - (Optional) PostgreSQL connection for production

### 4. Run the Hub Locally

```bash
cd orquestador
python main.py
```

The server will start at `http://localhost:8000/`

### 5. Access the Applications

**Dashboard (Lobby):**
- http://localhost:8000/

**Plant Detect Yourself (IA):**
- http://localhost:8000/plant-detect/

**Employees Manager:**
- http://localhost:8000/employees/

**To-Do List:**
- http://localhost:8000/todo/

---

## Project Structure

```
├── orquestador/                    # Central FastAPI hub
│   ├── apps/
│   │   ├── todo_list/             # To-Do List app
│   │   ├── employees/             # Employees Manager app
│   │   └── plant_detect/          # Plant Detect AI app
│   ├── main.py                    # Main entry point
│   ├── database.py                # SQLAlchemy config
│   ├── requirements.txt           # Python dependencies
│   └── .env.example              # Environment template
│
├── projects/                      # Standalone project folders
│   ├── todo_list/
│   ├── employees_manager/
│   └── plant_detect/
│
└── README.md                      # Project overview
```

---

## Available APIs

### Plant Detect
**Endpoint:** `POST /api/plants/identify`

**Request:**
```bash
curl -X POST http://localhost:8000/api/plants/identify \
  -F "file=@plant_photo.jpg" \
  -F "lang=es"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "is_plant": true,
    "results": [
      {
        "common_name": "Rose",
        "scientific_name": "Rosa spp.",
        "confidence_percentage": 95,
        "description": "...",
        "care_tips": [...],
        "toxicity": "safe",
        "origin": "Asia",
        "fun_fact": "..."
      }
    ]
  }
}
```

### Employees Manager
**Endpoints:**
- `GET /api/employees` - List employees
- `POST /api/employees` - Create employee
- `PUT /api/employees/{id}` - Update employee
- `PATCH /api/employees/{id}/retire` - Retire employee

### To-Do List
**Endpoints:**
- `GET /api/tasks` - List tasks
- `POST /api/tasks` - Create task
- `PATCH /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

---

## Deployment (Render.com)

The app is configured for deployment on Render:

**Build Command:**
```
cd orquestador && pip install -r requirements.txt
```

**Start Command:**
```
cd orquestador && uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Environment Variables on Render:**
- `DATABASE_URL` - PostgreSQL from Supabase
- `GROQ_API_KEY` - Your Groq API key

---

## Technologies Used

**Backend:**
- FastAPI - Modern Python web framework
- SQLAlchemy - ORM for database operations
- Pydantic - Data validation
- Groq API - AI for plant identification

**Frontend:**
- React 19 - UI library
- Vite - Frontend build tool
- Tailwind CSS - Styling
- Vanilla JS - For some modules

**Database:**
- PostgreSQL (Supabase) - Production
- SQLite - Local development

**Deployment:**
- Render.com - Hosting platform

---

## Troubleshooting

**ModuleNotFoundError: No module named 'groq'**
```bash
pip install groq
```

**Port 8000 already in use**
```bash
# Use a different port
uvicorn main:app --port 8001
```

**Plant Detect returns "Error de conexión"**
- Check that `GROQ_API_KEY` is set in `.env`
- Verify image format is valid (JPG, PNG)
- Check uvicorn logs for detailed errors

---

## Next Steps

- Add unit tests
- Implement CI/CD with GitHub Actions
- Add more plant detection features
- Integrate additional AI services

---

For more details, see the main [README.md](README.md)
