from flask import Flask, render_template

app = Flask(__name__)

@app.route('/productos')
def productos():
    # Example data (Usually this comes from a database)
    lista_productos = [
        {'id': 1, 'nombre': 'Martillo', 'categoria': 'Herramientas', 'precio': 15.00, 'stock': 50},
        {'id': 2, 'nombre': 'Clavos 2"', 'categoria': 'Ferretería', 'precio': 0.05, 'stock': 1000},
    ]
    return render_template('productos.html', productos=lista_productos)