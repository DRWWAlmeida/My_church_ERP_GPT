from app.errors import errors_bp

from app.modules.category.routes import category_bp
from app.modules.checking_account.routes import checking_account_bp


def register_blueprints(app):
    app.register_blueprint(errors_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(checking_account_bp)
