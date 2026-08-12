import sqlite3
from flask import current_app
from app.config import DB_PATH

def get_connection():
    try:
        db_target = current_app.config.get('DATABASE', DB_PATH)
    except RuntimeError:
        db_target = DB_PATH

    connection = sqlite3.connect(db_target)
    connection.execute('PRAGMA foreign_keys = ON;')
    return connection