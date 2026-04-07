from .routes.contas_correntes import contas_correntes_bp
from .routes.tipo_lancamentos import tipo_lancamentos_bp
from .routes.home import home_bp



def register_blueprints(app):
    app.register_blueprint(contas_correntes_bp)
    app.register_blueprint(tipo_lancamentos_bp)
    app.register_blueprint(home_bp)

