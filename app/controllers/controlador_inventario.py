from flask import Blueprint, render_template, request, redirect, url_for
from app.services import servicio_inventario as service
from app.services import servicio_producto
from app.services import servicio_almacen

bp = Blueprint('inventario', __name__, url_prefix='/inventario')

@bp.route('')
def inventario():
    lista = service.obtener_todo_inventario()
    return render_template('inventario.html', inventario=lista)

@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_inventario():
    if request.method == 'POST':
        id_producto = request.form.get('id_producto')
        id_almacen  = request.form.get('id_almacen')
        cantidad    = request.form.get('cantidad')

        ok, msg = service.crear_inventario(id_producto, id_almacen, cantidad)

        if ok:
            return redirect(url_for('inventario.inventario'))
        else:
            productos = servicio_producto.obtener_todos_productos()
            almacenes = servicio_almacen.obtener_todos_almacenes()
            return render_template('nuevo_inventario.html', 
                                   productos=productos,
                                   almacenes=almacenes,
                                   error=msg)

    productos = servicio_producto.obtener_todos_productos()
    almacenes = servicio_almacen.obtener_todos_almacenes()
    return render_template('nuevo_inventario.html',
                           productos=productos,
                           almacenes=almacenes)

@bp.route('/editar/<int:id_producto>/<int:id_almacen>', methods=['GET', 'POST'])
def editar_inventario(id_producto, id_almacen):
    if request.method == 'POST':
        cantidad = request.form.get('cantidad')
        ok, msg = service.actualizar_stock_inventario(id_producto, id_almacen, cantidad)
        if ok:
            return redirect(url_for('inventario.inventario'))
        else:
            return render_template('editar_inventario.html', 
                                   id_producto=id_producto,
                                   id_almacen=id_almacen,
                                   error=msg)

    return render_template('editar_inventario.html',
                           id_producto=id_producto,
                           id_almacen=id_almacen)

@bp.route('/eliminar/<int:id_producto>/<int:id_almacen>', methods=['POST'])
def eliminar_inventario(id_producto, id_almacen):
    service.eliminar_inventario(id_producto, id_almacen)
    return redirect(url_for('inventario.inventario'))
