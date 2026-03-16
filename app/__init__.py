from flask import Flask
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Registrar Blueprint principal
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app





""""
from flask import Flask,render_template
from config import Config

app = Flask(__name__)

@app.route('/')
def hub():
    return render_template('hub.html')

@app.route('/productos')
def productos():
    return "Página de Productos"

@app.route('/almacenes')
def almacenes():
    return "Página de Almacenes"

@app.route('/inventario')
def inventario():
    return "Página de Inventario"

if __name__ == '__main__':
    app.run(debug=True)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
"""