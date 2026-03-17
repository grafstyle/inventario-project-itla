from flask import Flask
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Registrar Blueprint principal
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Registrar Blueprints de módulos
    from app.modules.productos import bp as productos_bp
    app.register_blueprint(productos_bp)

    from app.modules.almacenes import bp as almacenes_bp
    app.register_blueprint(almacenes_bp)

    from app.modules.inventario import bp as inventario_bp
    app.register_blueprint(inventario_bp)

    return app
