from flask import Blueprint, render_template, request, redirect, url_for
from app.services import servicio_producto as service

bp = Blueprint('productos', __name__, url_prefix='/productos')

@bp.route('')
def productos():
    lista = service.obtener_todos_productos()
    return render_template('productos.html', productos=lista)

@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        nombre      = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio      = request.form.get('precio')
        costo       = request.form.get('costo')

        ok, msg, _ = service.crear_producto(nombre, descripcion, precio, costo)

        if ok:
            return redirect(url_for('productos.productos'))
        else:
            return render_template('nuevo_producto.html', error=msg)

    return render_template('nuevo_producto.html')

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = service.obtener_producto(id)
    if not producto:
        return redirect(url_for('productos.productos'))

    if request.method == 'POST':
        nombre      = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio      = request.form.get('precio')
        costo       = request.form.get('costo')

        ok, msg = service.actualizar_producto(id, nombre, descripcion, precio, costo)

        if ok:
            return redirect(url_for('productos.productos'))
        else:
            return render_template('editar_producto.html', p=producto, error=msg)

    return render_template('editar_producto.html', p=producto)


@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    service.eliminar_producto(id)
    return redirect(url_for('productos.productos'))
