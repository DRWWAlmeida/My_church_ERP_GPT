from .routes.contas_correntes import contas_correntes_bp
from .routes.tipo_lancamentos import tipo_lancamentos_bp
from .routes.home import home_bp
from .routes.categorias import categorias_bp
from .routes.lancamentos import lancamentos_bp



def register_blueprints(app):
    app.register_blueprint(contas_correntes_bp)
    app.register_blueprint(tipo_lancamentos_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(lancamentos_bp)
