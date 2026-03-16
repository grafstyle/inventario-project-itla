from flask import Blueprint, render_template, request, redirect, url_for
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'db'))
import database as db
import logic as lg

bp = Blueprint('main', __name__)

db.init_db()

@bp.route('/')
def index():
    return render_template('hub.html')


# ── Productos ────────────────────────────────

@bp.route('/productos')
def productos():
    lista = db.get_all_products()
    return render_template('productos.html', productos=lista)

@bp.route('/productos/nuevo', methods=['GET', 'POST'])
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
            return redirect(url_for('main.productos'))
        else:
            return render_template('nuevo_producto.html', error=msg)

    return render_template('nuevo_producto.html')

@bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = db.get_product(id)
    if not producto:
        return redirect(url_for('main.productos'))

    if request.method == 'POST':
        name        = request.form.get('name')
        description = request.form.get('description')
        price       = request.form.get('price')
        cost        = request.form.get('cost')

        ok, msg = lg.logic_update_product(id, name, description, price, cost)

        if ok:
            return redirect(url_for('main.productos'))
        else:
            return render_template('editar_producto.html', producto=producto, error=msg)

    return render_template('editar_producto.html', producto=producto)


@bp.route('/productos/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    lg.logic_delete_product(id)
    return redirect(url_for('main.productos'))

# ── Almacenes ────────────────────────────────

@bp.route('/almacenes')
def almacenes():
    lista = db.get_all_warehouses()
    return render_template('almacenes.html', almacenes=lista)

@bp.route('/almacenes/nuevo', methods=['GET', 'POST'])
def nuevo_almacen():
    if request.method == 'POST':
        name    = request.form.get('name')
        country = request.form.get('country')
        city    = request.form.get('city')

        ok, msg = lg.logic_create_warehouse(name, country, city)

        if ok:
            return redirect(url_for('main.almacenes'))
        else:
            return render_template('nuevo_almacen.html', error=msg)

    return render_template('nuevo_almacen.html')

@bp.route('/almacenes/editar/<int:id>', methods=['GET', 'POST'])
def editar_almacen(id):
    almacen = db.get_warehouse(id)
    if not almacen:
        return redirect(url_for('main.almacenes'))

    if request.method == 'POST':
        name    = request.form.get('name')
        country = request.form.get('country')
        city    = request.form.get('city')

        ok, msg = lg.logic_update_warehouse(id, name, country, city)

        if ok:
            return redirect(url_for('main.almacenes'))
        else:
            return render_template('editar_almacen.html', almacen=almacen, error=msg)

    return render_template('editar_almacen.html', almacen=almacen)

@bp.route('/almacenes/eliminar/<int:id>', methods=['POST'])
def eliminar_almacen(id):
    lg.logic_delete_warehouse(id)
    return redirect(url_for('main.almacenes'))

# ── Inventario ───────────────────────────────

@bp.route('/inventario')
def inventario():
    lista = db.get_all_inventory()
    return render_template('inventario.html', inventario=lista)

@bp.route('/inventario/nuevo', methods=['GET', 'POST'])
def nuevo_inventario():
    if request.method == 'POST':
        idProduct   = request.form.get('idProduct')
        idWarehouse = request.form.get('idWarehouse')
        stock       = request.form.get('stock')

        ok, msg = lg.logic_create_inventory(idProduct, idWarehouse, stock)

        if ok:
            return redirect(url_for('main.inventario'))
        else:
            productos = db.get_all_products()
            almacenes = db.get_all_warehouses()
            return render_template('nuevo_inventario.html', 
                                   productos=productos,
                                   almacenes=almacenes,
                                   error=msg)

    productos = db.get_all_products()
    almacenes = db.get_all_warehouses()
    return render_template('nuevo_inventario.html',
                           productos=productos,
                           almacenes=almacenes)

@bp.route('/inventario/editar/<int:idProduct>/<int:idWarehouse>', methods=['GET', 'POST'])
def editar_inventario(idProduct, idWarehouse):
    if request.method == 'POST':
        stock = request.form.get('stock')
        ok, msg = lg.logic_update_inventory_stock(idProduct, idWarehouse, stock)
        if ok:
            return redirect(url_for('main.inventario'))
        else:
            return render_template('editar_inventario.html', 
                                   idProduct=idProduct,
                                   idWarehouse=idWarehouse,
                                   error=msg)

    return render_template('editar_inventario.html',
                           idProduct=idProduct,
                           idWarehouse=idWarehouse)

@bp.route('/inventario/eliminar/<int:idProduct>/<int:idWarehouse>', methods=['POST'])
def eliminar_inventario(idProduct, idWarehouse):
    lg.logic_delete_inventory(idProduct, idWarehouse)
    return redirect(url_for('main.inventario'))