# Projects Hub - Orquestador

Hub centralizado para acceder y orquestar todos tus proyectos en un solo lugar.

## 🚀 Estructura Escalable

```
orquestador/
├── main.py                 # FastAPI que lee projects.json dinámicamente
├── data/
│   └── projects.json       # 📌 ARCHIVO CLAVE: Lista de proyectos
├── static/
│   └── images/             # 📌 Imágenes de proyectos
├── templates/
│   └── dashboard.html      # Template dinámico (no edites esto para agregar proyectos)
└── .gitignore
```

## 🎯 Cómo Agregar un Nuevo Proyecto (3 pasos simples)

### 1️⃣ Edita `data/projects.json`

Agrega un nuevo objeto en el array `projects`:

```json
{
  "id": "mi-nuevo-proyecto",
  "name": "Mi Nuevo Proyecto",
  "description": "Descripción breve y atractiva del proyecto",
  "image": "mi-nuevo-proyecto.png",
  "url": "/mi-ruta",
  "buttonText": "Botón CTA",
  "buttonColor": "from-red-600 to-pink-600",
  "hoverColor": "from-red-700 to-pink-700",
  "tags": ["Tech1", "Tech2", "Tech3"],
  "priority": 4
}
```

**Campos:**
- `id`: Identificador único (sin espacios, snake_case)
- `name`: Nombre mostrado
- `description`: Descripción (máx ~120 caracteres)
- `image`: Nombre archivo (ej: `mi-proyecto.png`)
- `url`: Ruta relativa (ej: `/mi-proyecto`)
- `buttonText`: Texto del botón CTA
- `buttonColor` y `hoverColor`: Colores Tailwind (ej: `from-purple-600 to-blue-600`)
- `tags`: Array de tecnologías (máx 3)
- `priority`: Orden en el grid (1, 2, 3, etc.)

### 2️⃣ Coloca la imagen en `static/images/`

Agrega tu imagen en la carpeta `static/images/`:
- Formato recomendado: **PNG o JPG**
- Tamaño recomendado: **600x400px** (16:9)
- Nombre: **igual al especificado en JSON** (ej: `mi-nuevo-proyecto.png`)

### 3️⃣ Implementa la ruta en `main.py`

Si tu proyecto es externo (en otra carpeta), crea una ruta que lo sirva:

```python
@app.get("/mi-ruta", response_class=HTMLResponse)
async def get_mi_proyecto():
    """Ruta para Mi Nuevo Proyecto"""
    # TODO: Conectar con la app real
    return HTMLResponse(content="<h1>Mi Nuevo Proyecto</h1>")
```

O si ya existe una app corriendo en otro puerto, puedes hacer un proxy:

```python
from fastapi.responses import RedirectResponse

@app.get("/mi-ruta")
async def get_mi_proyecto():
    return RedirectResponse(url="http://localhost:3000")  # O el puerto que uses
```

---

## 💻 Ejecutar el Hub

### Primera vez
```powershell
cd orquestador
python -m venv venv
.\venv\Scripts\Activate
pip install fastapi uvicorn
```

### Lanzar el servidor
```powershell
python main.py
```

O con uvicorn:
```powershell
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Abre: **http://localhost:8000**

---

## 🎨 Paleta de Colores Tailwind (para referencia)

```
from-purple-600 to-blue-600        (Púrpura → Azul)
from-blue-600 to-purple-600        (Azul → Púrpura)
from-cyan-600 to-blue-600          (Cian → Azul)
from-green-600 to-cyan-600         (Verde → Cian)
from-pink-600 to-red-600           (Rosa → Rojo)
from-yellow-600 to-orange-600      (Amarillo → Naranja)
from-indigo-600 to-purple-600      (Índigo → Púrpura)
```

---

## 🔧 API Endpoints

- `GET /` → Dashboard principal
- `GET /health` → Health check
- `GET /api/projects` → Lista de proyectos en JSON

---

## 💡 Tips

- **No edites `dashboard.html`** para agregar proyectos → usa solo `projects.json`
- Las imágenes se sirven automáticamente desde `static/images/`
- La prioridad ordena los proyectos (1 = primero)
- Puedes tener múltiples proyectos sin impacto en RAM si usas subrutas correctamente
