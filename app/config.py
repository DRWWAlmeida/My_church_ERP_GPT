import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

DEBUG = os.getenv("FLASK_DEBUG", "false").lower() in {"1", "true", "yes"}
TESTING = False

DB_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "db" / "igreja_erp.db"))
