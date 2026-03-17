from flask import Blueprint, render_template, request, redirect, url_for
from app.services import inventory_service as service
from app.services import product_service
from app.services import warehouse_service

bp = Blueprint('inventario', __name__, url_prefix='/inventario')

@bp.route('')
def inventario():
    lista = service.get_all_inventory()
    return render_template('inventario.html', inventario=lista)

@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_inventario():
    if request.method == 'POST':
        idProduct   = request.form.get('idProduct')
        idWarehouse = request.form.get('idWarehouse')
        stock       = request.form.get('stock')

        ok, msg = service.create_inventory(idProduct, idWarehouse, stock)

        if ok:
            return redirect(url_for('inventario.inventario'))
        else:
            productos = product_service.get_all_products()
            almacenes = warehouse_service.get_all_warehouses()
            return render_template('nuevo_inventario.html', 
                                   productos=productos,
                                   almacenes=almacenes,
                                   error=msg)

    productos = product_service.get_all_products()
    almacenes = warehouse_service.get_all_warehouses()
    return render_template('nuevo_inventario.html',
                           productos=productos,
                           almacenes=almacenes)

@bp.route('/editar/<int:idProduct>/<int:idWarehouse>', methods=['GET', 'POST'])
def editar_inventario(idProduct, idWarehouse):
    if request.method == 'POST':
        stock = request.form.get('stock')
        ok, msg = service.update_inventory_stock(idProduct, idWarehouse, stock)
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
    service.delete_inventory(idProduct, idWarehouse)
    return redirect(url_for('inventario.inventario'))
