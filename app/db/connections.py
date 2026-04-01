import sqlite3

DB_PATH = 'app/models/igreja_erp.db'

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.execute('PRAGMA foreign_keys = ON;')
    return connection

