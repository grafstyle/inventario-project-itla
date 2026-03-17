from flask import Flask
from config import Config
from app.repositories.db_config import init_db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar Base de Datos
    init_db()

    # Registrar Blueprint principal
    from app.controllers.main_controller import bp as main_bp
    app.register_blueprint(main_bp)

    # Registrar Blueprints de controladores
    from app.controllers.product_controller import bp as productos_bp
    app.register_blueprint(productos_bp)

    from app.controllers.warehouse_controller import bp as almacenes_bp
    app.register_blueprint(almacenes_bp)

    from app.controllers.inventory_controller import bp as inventario_bp
    app.register_blueprint(inventario_bp)

    return app
