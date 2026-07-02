from flask import Flask
from app.api import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config")

    register_blueprints(app)
    return app
