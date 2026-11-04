import os
import sqlite3
from flask import current_app, has_app_context
from app import config

def get_connection():
    if has_app_context():
        settings = current_app.config
        db_target = settings['DATABASE'] if 'DATABASE' in settings else settings['DB_PATH']
    else:
        db_target = config.DB_PATH

    if isinstance(db_target, os.PathLike):
        db_target = os.fspath(db_target)
    if not isinstance(db_target, str) or not db_target.strip():
        raise ValueError('O destino do banco deve ser um caminho não vazio.')

    connection = sqlite3.connect(db_target)
    connection.execute('PRAGMA foreign_keys = ON;')
    return connection
