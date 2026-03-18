from flask import Blueprint, render_template, request, redirect, url_for
from app.services import servicio_inventario as servicio
from app.services import servicio_producto
from app.services import servicio_almacen

bp = Blueprint('inventario', __name__, url_prefix='/inventario')


@bp.route('')
def inventario():
    """Muestra la lista completa del inventario."""
    lista = servicio.obtener_todo_inventario()
    return render_template('inventario.html', inventario=lista)


@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_inventario():
    """Muestra el formulario para agregar stock. Si es POST, guarda el registro."""
    if request.method == 'POST':
        # Leemos los datos del formulario
        id_producto = request.form.get('id_producto')
        id_almacen  = request.form.get('id_almacen')
        cantidad    = request.form.get('cantidad')

        # Le pedimos al servicio que cree el registro
        exito, mensaje = servicio.crear_inventario(id_producto, id_almacen, cantidad)

        if exito:
            return redirect(url_for('inventario.inventario'))
        else:
            # Si hubo error, volvemos al formulario con los dropdown y el error
            productos = servicio_producto.obtener_todos_productos()
            almacenes = servicio_almacen.obtener_todos_almacenes()
            return render_template('nuevo_inventario.html',
                                   productos=productos,
                                   almacenes=almacenes,
                                   error=mensaje)

    # Si es GET, cargamos los productos y almacenes para los dropdown
    productos = servicio_producto.obtener_todos_productos()
    almacenes = servicio_almacen.obtener_todos_almacenes()
    return render_template('nuevo_inventario.html',
                           productos=productos,
                           almacenes=almacenes)


@bp.route('/editar/<int:id_producto>/<int:id_almacen>', methods=['GET', 'POST'])
def editar_inventario(id_producto, id_almacen):
    """Muestra el formulario para editar el stock. Si es POST, lo actualiza."""
    if request.method == 'POST':
        cantidad = request.form.get('cantidad')
        exito, mensaje = servicio.actualizar_stock_inventario(id_producto, id_almacen, cantidad)

        if exito:
            return redirect(url_for('inventario.inventario'))
        else:
            return render_template('editar_inventario.html',
                                   id_producto=id_producto,
                                   id_almacen=id_almacen,
                                   error=mensaje)

    return render_template('editar_inventario.html',
                           id_producto=id_producto,
                           id_almacen=id_almacen)


@bp.route('/eliminar/<int:id_producto>/<int:id_almacen>', methods=['POST'])
def eliminar_inventario(id_producto, id_almacen):
    """Elimina el registro de inventario y redirige a la lista."""
    servicio.eliminar_inventario(id_producto, id_almacen)
    return redirect(url_for('inventario.inventario'))
