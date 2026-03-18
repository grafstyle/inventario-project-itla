from flask import Blueprint, render_template, request, redirect, url_for
from app.services import servicio_producto as servicio

bp = Blueprint('productos', __name__, url_prefix='/productos')


@bp.route('')
def productos():
    """Muestra la lista de todos los productos."""
    lista = servicio.obtener_todos_productos()
    return render_template('productos.html', productos=lista)


@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    """Muestra el formulario para crear un producto. Si es POST, guarda el producto."""
    if request.method == 'POST':
        # Leemos los datos del formulario
        nombre      = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio      = request.form.get('precio')
        costo       = request.form.get('costo')

        # Le pedimos al servicio que lo cree
        exito, mensaje, _ = servicio.crear_producto(nombre, descripcion, precio, costo)

        if exito:
            # Si tuvo exito, redirigimos a la lista de productos
            return redirect(url_for('productos.productos'))
        else:
            # Si hubo un error, mostramos el formulario con el mensaje de error
            return render_template('nuevo_producto.html', error=mensaje)

    # Si es GET, simplemente mostramos el formulario vacio
    return render_template('nuevo_producto.html')


@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    """Muestra el formulario para editar un producto. Si es POST, lo actualiza."""
    # Buscamos el producto que queremos editar
    producto = servicio.obtener_producto(id)

    # Si no existe, volvemos a la lista
    if not producto:
        return redirect(url_for('productos.productos'))

    if request.method == 'POST':
        nombre      = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio      = request.form.get('precio')
        costo       = request.form.get('costo')

        exito, mensaje = servicio.actualizar_producto(id, nombre, descripcion, precio, costo)

        if exito:
            return redirect(url_for('productos.productos'))
        else:
            return render_template('editar_producto.html', p=producto, error=mensaje)

    return render_template('editar_producto.html', p=producto)


@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    """Elimina el producto indicado y redirige a la lista."""
    servicio.eliminar_producto(id)
    return redirect(url_for('productos.productos'))
