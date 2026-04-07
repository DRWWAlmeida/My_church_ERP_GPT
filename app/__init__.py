from flask import Flask

from app.api import register_blueprints
from app.db.schema import create_schema


def create_app():
    app = Flask(__name__)

    create_schema()
    register_blueprints(app)

    return app
