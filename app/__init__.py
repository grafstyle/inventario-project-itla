from flask import Flask
from config import Config
from app.repositories.config_bd import inicializar_bd

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar Base de Datos
    inicializar_bd()

    # Registrar Blueprint principal
    from app.controllers.controlador_principal import bp as main_bp
    app.register_blueprint(main_bp)

    # Registrar Blueprints de controladores
    from app.controllers.controlador_producto import bp as productos_bp
    app.register_blueprint(productos_bp)

    from app.controllers.controlador_almacen import bp as almacenes_bp
    app.register_blueprint(almacenes_bp)

    from app.controllers.controlador_inventario import bp as inventario_bp
    app.register_blueprint(inventario_bp)

    return app
