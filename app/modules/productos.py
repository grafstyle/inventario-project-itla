from flask import Blueprint, render_template, request, redirect, url_for
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db'))
import database as db
import logic as lg

bp = Blueprint('productos', __name__, url_prefix='/productos')

@bp.route('')
def productos():
    lista = db.get_all_products()
    return render_template('productos.html', productos=lista)

@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        # Recoger datos del formulario
        name        = request.form.get('name')
        description = request.form.get('description')
        price       = request.form.get('price')
        cost        = request.form.get('cost')

        # Validar con logic.py
        ok, msg = lg.logic_create_product(name, description, price, cost)

        if ok:
            return redirect(url_for('productos.productos'))
        else:
            return render_template('nuevo_producto.html', error=msg)

    return render_template('nuevo_producto.html')

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = db.get_product(id)
    if not producto:
        return redirect(url_for('productos.productos'))

    if request.method == 'POST':
        name        = request.form.get('name')
        description = request.form.get('description')
        price       = request.form.get('price')
        cost        = request.form.get('cost')

        ok, msg = lg.logic_update_product(id, name, description, price, cost)

        if ok:
            return redirect(url_for('productos.productos'))
        else:
            return render_template('editar_producto.html', producto=producto, error=msg)

    return render_template('editar_producto.html', producto=producto)


@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    lg.logic_delete_product(id)
    return redirect(url_for('productos.productos'))