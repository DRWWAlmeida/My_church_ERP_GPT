from app.errors import errors_bp

from app.modules.category.routes import category_bp



def register_blueprints(app):
    app.register_blueprint(errors_bp)
    app.register_blueprint(category_bp)
