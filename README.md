# 🚀 Projects Hub - API Gateway Unificado

**Developer:** Juan José Meneses Jaramillo  
**GitHub:** [@Menesex](https://github.com/Menesex)

---

## 📌 ¿Qué es esto?

Un **orquestador central eficiente** que unifica múltiples proyectos independientes bajo una sola IP y servidor. En lugar de mantener cada proyecto en instancias separadas (consumiendo RAM y costos), todo se sirve desde **un único proceso FastAPI**, manteniendo escalabilidad y flexibilidad.

Es el **corazón visual y enrutador** de mi portafolio técnico, optimizado para hosting gratuito con limitaciones estrictas (512MB RAM).

---

## 💡 ¿Por qué lo hice así?

### Problema Original
- Múltiples proyectos requieren hosting separado → **múltiples instancias = más RAM = más costo**
- Cada proyecto hibernaría por inactividad en servidores free → **experiencia lenta**
- Gestionar credenciales y configuración dispersa en N lugares → **caos operacional**

### Solución: Orquestación Centralizada
✅ **Un único servidor FastAPI** sirve todos los proyectos  
✅ **Arquitectura escalable**: agregar proyectos = editar 1 archivo JSON  
✅ **Bajo consumo de RAM**: carpetas estáticas + sub-apps compartiendo proceso  
✅ **Desacoplado**: cada proyecto vive en su propia carpeta, sin dependencias cruzadas  
✅ **Production-ready**: listo para Render, Vercel, Railway o cualquier PaaS

---

## 🏗️ Estructura del Monorrepósito

```
MeneProjectPortfolio/
│
├── orquestador/                          # 🎯 El Hub central (FastAPI)
│   ├── main.py                          # Servidor + orquestación
│   ├── requirements.txt                 # Dependencias minimalistas
│   ├── Procfile                         # Config para Render
│   ├── templates/
│   │   └── dashboard.html               # UI dinámica (Tailwind CSS)
│   ├── data/
│   │   └── projects.json                # 📌 Configuración centralizada
│   ├── static/
│   │   └── images/                      # Screenshots de proyectos
│   └── .gitignore
│
├── 1-todo-list/                         # 📝 Proyecto 1: To-Do List (Static)
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── 2-employees-manager/                 # 👥 Proyecto 2: API Backend (FastAPI)
│   ├── main.py
│   ├── requirements.txt
│   └── ...
│
├── 3-polygraphix/                       # 📊 Proyecto 3: Data Visualizer (Streamlit)
│   ├── app.py
│   ├── requirements.txt
│   └── ...
│
├── .env                                 # 🔐 Variables locales (gitignored)
├── .env.example                         # 📋 Template de variables
├── .gitignore                           # Configuración global
└── README.md                            # Este archivo
```

---

## 🎯 Cómo Funciona

### 1. **Hub Central (Orquestador)**
- Levanta en puerto 8000 (o el que asigne Render)
- Lee dinámicamente `projects.json`
- Renderiza dashboard interactivo
- Monta carpetas estáticas con `StaticFiles`

### 2. **Proyectos Servidos**
- **1-todo-list**: Montada como carpeta estática en `/todo`
- **2-employees-manager**: Backend FastAPI con su propia lógica (futuro)
- **3-polygraphix**: Streamlit hosteado internamente (futuro)

### 3. **Configuración Dinámica**
Solo edita `orquestador/data/projects.json`:

```json
{
  "projects": [
    {
      "id": "todo-list",
      "name": "Interactive To-Do List",
      "url": "/todo",
      "buttonText": "Abrir Aplicación",
      "tags": ["HTML5", "CSS3", "JavaScript"],
      "priority": 2
    }
  ]
}
```

**Agregar nuevo proyecto = 1 entrada JSON + carpeta + imagen**. Sin tocar código.

---

## 🚀 Instalación y Ejecución

### Requisitos
- Python 3.9+
- pip

### Local (Desarrollo)

```powershell
# 1. Clonar y navegar
git clone <repo-url>
cd orquestador

# 2. Entorno virtual
python -m venv venv
.\venv\Scripts\Activate

# 3. Dependencias
pip install -r requirements.txt

# 4. Ejecutar
python main.py
```

Abre: **http://localhost:8000**

### Production (Render, Railway, etc.)

1. Push a GitHub
2. Conecta el repo a tu plataforma free (Render, Railway)
3. Apunta a carpeta: `orquestador/`
4. Render detecta `Procfile` y lanza automáticamente
5. ✅ Tu hub está live

---

## 📊 Arquitectura Técnica

### Stack
- **Backend**: FastAPI (ultra ligero)
- **Frontend**: Tailwind CSS + Jinja2 Templates
- **Hosting**: Render / Railway / Vercel (free tier)
- **Control**: Git + GitHub

### Optimizaciones para RAM (512MB)
- ✅ Cero dependencias pesadas (no Django, no SQLAlchemy en el hub)
- ✅ StaticFiles mounting (sirve folders sin procesar)
- ✅ JSON config (sin base de datos central)
- ✅ Sub-apps compartiendo proceso (no multiprocess)
- ✅ HTML estático + Tailwind vía CDN

### Escalabilidad
- Agregar proyecto nuevo = editar `projects.json` + subir carpeta
- No hay límite de proyectos (mientras quepa en 512MB)
- Cada proyecto aislado en su carpeta (actualizaciones sin romper hub)

---

## 📝 Proyectos Integrados

| Proyecto | Tipo | Tech Stack | Estado |
|----------|------|-----------|--------|
| **Interactive To-Do List** | Frontend | HTML5, CSS3, JS | ✅ Live |
| **Employees Manager** | Backend | FastAPI, PostgreSQL | 🔄 Próximo |
| **PolyGraphiX Visualizer** | Data/Viz | Python, Streamlit | 🔄 Próximo |

---

## 🔐 Variables de Entorno

Copia `.env.example` a `.env` y rellena:

```bash
# .env
DATABASE_URL=postgresql://...
SECRET_KEY=tu-clave-segura
ENVIRONMENT=production
```

El archivo `.env` está en `.gitignore` por seguridad.

---

## 🛠️ Comandos Útiles

```bash
# Desarrollo
uvicorn main:app --reload

# Testing local
curl http://localhost:8000/api/projects

# Ver estructura
tree /F

# Subir cambios
git add .
git commit -m "message"
git push
```

---

## 📚 Documentación Adicional

- **[Orquestador](./orquestador/README.md)** - Cómo agregar proyectos
- **[To-Do List](./1-todo-list/)** - Documentación del proyecto
- **[Employees Manager](./2-employees-manager/)** - (Próximo)

---

## 🎨 UI/UX

- **Dashboard**: Minimalista y funcional (no overshadow proyectos)
- **Tarjetas**: Dinámicas, con hover effects
- **Imágenes**: Espacio reservado 600x400px recomendado
- **Colores**: Gradientes Tailwind por proyecto

---

## 🚨 Notas de Desarrollo

- Cada proyecto es **completamente independiente**
- El hub solo **ensambla y sirve**
- Para actualizar un proyecto: push a su carpeta, sin tocar el orquestador
- Si un proyecto se cae: el hub sigue vivo
- Secretos en `.env`, nunca en código

---

## 📞 Contacto

📧 **Email**: juanmenesesjara@gmail.com  
🐙 **GitHub**: [@Menesex](https://github.com/Menesex)  
🔗 **LinkedIn**: [Juan José Meneses](https://linkedin.com/in/juan-meneses)

---

**© 2026 Juan José Meneses Jaramillo** | Ingeniero de Software  
*"Simple, efficient, scalable."*
