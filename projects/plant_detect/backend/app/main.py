from fastapi import FastAPI
from app.api.endpoints import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="🌿 Bio AI API", version="1.0.0")

# --- CONFIGURACIÓN DE CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción pondrás la URL de tu Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------------

app.include_router(router, prefix="/api") #"Cualquier ruta que venga de endpoints.py, ponle el prefijo /api antes".

@app.get("/")
def root():
    return {"status": "ok", "message": "Bio AI backend running"}

#Como en endpoints.py definiste @router.post("/identify"), la ruta completa que el mundo ve es:
#dominio.com/api/identify