import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent
env_file = BASE_DIR / ".env"

# ✅ EXPLICIT LOAD WITH DEBUG
print("\n" + "="*70)
print("🔍 ENVIRONMENT LOADING DEBUG")
print("="*70)
print(f"📂 Looking for .env at: {env_file}")
print(f"✓ .env exists: {env_file.exists()}")

load_dotenv(env_file, override=True)

_raw_url = os.getenv("DATABASE_URL")

if _raw_url:
    print(f"✓ DATABASE_URL found in environment")

    # Parse URL to show components (without password)
    parsed = urlparse(_raw_url)
    safe_url = f"{parsed.scheme}://{parsed.username}@{parsed.hostname}:{parsed.port}/{parsed.path.lstrip('/')}"
    print(f"  User: {parsed.username}")
    print(f"  Host: {parsed.hostname}")
    print(f"  Port: {parsed.port}")
    print(f"  Database: {parsed.path.lstrip('/')}")
    print(f"  Safe URL: {safe_url}")

    # Fix postgres:// → postgresql://
    DATABASE_URL = _raw_url.replace("postgres://", "postgresql://", 1)
    DB_TYPE = "PostgreSQL (Supabase)"

    print(f"\n✓ Using: {DB_TYPE}")
    engine = create_engine(DATABASE_URL, echo=False)

else:
    print(f"✗ DATABASE_URL NOT found in environment")
    print(f"  Falling back to SQLite local")

    # Desarrollo local: SQLite
    DATA_DIR = BASE_DIR / "data"
    DATA_DIR.mkdir(exist_ok=True)
    DATABASE_URL = f"sqlite:///{DATA_DIR}/app.db"
    DB_TYPE = "SQLite (Local)"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    print(f"✓ Using: {DB_TYPE}")

print("="*70 + "\n")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Lazy initialization flag
_db_initialized = False


def init_db():
    """Create all registered tables. Called lazily on first API use."""
    global _db_initialized
    if _db_initialized:
        return

    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created/verified successfully")
        _db_initialized = True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise


def verify_db_connection():
    """Test connection to database. Run once on first use."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection verified")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def get_db():
    """Dependency for routes. Lazily initializes DB on first use."""
    global _db_initialized
    if not _db_initialized:
        verify_db_connection()
        init_db()

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
