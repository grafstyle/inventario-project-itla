from flask import Blueprint, render_template, request, redirect, url_for
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db'))
import database as db
import logic as lg

bp = Blueprint('inventario', __name__, url_prefix='/inventario')

@bp.route('')
def inventario():
    lista = db.get_all_inventory()
    return render_template('inventario.html', inventario=lista)

@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_inventario():
    if request.method == 'POST':
        idProduct   = request.form.get('idProduct')
        idWarehouse = request.form.get('idWarehouse')
        stock       = request.form.get('stock')

        ok, msg = lg.logic_create_inventory(idProduct, idWarehouse, stock)

        if ok:
            return redirect(url_for('inventario.inventario'))
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

@bp.route('/editar/<int:idProduct>/<int:idWarehouse>', methods=['GET', 'POST'])
def editar_inventario(idProduct, idWarehouse):
    if request.method == 'POST':
        stock = request.form.get('stock')
        ok, msg = lg.logic_update_inventory_stock(idProduct, idWarehouse, stock)
        if ok:
            return redirect(url_for('inventario.inventario'))
        else:
            return render_template('editar_inventario.html', 
                                   idProduct=idProduct,
                                   idWarehouse=idWarehouse,
                                   error=msg)

    return render_template('editar_inventario.html',
                           idProduct=idProduct,
                           idWarehouse=idWarehouse)

@bp.route('/eliminar/<int:idProduct>/<int:idWarehouse>', methods=['POST'])
def eliminar_inventario(idProduct, idWarehouse):
    lg.logic_delete_inventory(idProduct, idWarehouse)
    return redirect(url_for('inventario.inventario'))
