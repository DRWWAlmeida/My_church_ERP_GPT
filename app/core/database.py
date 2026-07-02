import sqlite3
from app.config import DB_PATH

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.execute('PRAGMA foreign_keys = ON;')
    return connection