from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

DEBUG = True
TESTING = False

DB_PATH = str(PROJECT_ROOT / "app" / "db" / "igreja_erp.db")
