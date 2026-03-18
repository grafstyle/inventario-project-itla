from flask import Blueprint, render_template, request, redirect, url_for
from app.services import servicio_almacen as servicio

bp = Blueprint('almacenes', __name__, url_prefix='/almacenes')


@bp.route('')
def almacenes():
    """Muestra la lista de todos los almacenes."""
    lista = servicio.obtener_todos_almacenes()
    return render_template('almacenes.html', almacenes=lista)


@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_almacen():
    """Muestra el formulario para crear un almacen. Si es POST, guarda el almacen."""
    if request.method == 'POST':
        # Leemos los datos del formulario
        nombre = request.form.get('nombre')
        pais   = request.form.get('pais')
        ciudad = request.form.get('ciudad')

        # Le pedimos al servicio que lo cree
        exito, mensaje, _ = servicio.crear_almacen(nombre, pais, ciudad)

        if exito:
            # Si tuvo exito, redirigimos a la lista de almacenes
            return redirect(url_for('almacenes.almacenes'))
        else:
            # Si hubo un error, mostramos el formulario con el mensaje de error
            return render_template('nuevo_almacen.html', error=mensaje)

    # Si es GET, simplemente mostramos el formulario vacio
    return render_template('nuevo_almacen.html')


@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_almacen(id):
    """Muestra el formulario para editar un almacen. Si es POST, lo actualiza."""
    # Buscamos el almacen que queremos editar
    almacen = servicio.obtener_almacen(id)

    # Si no existe, volvemos a la lista
    if not almacen:
        return redirect(url_for('almacenes.almacenes'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        pais   = request.form.get('pais')
        ciudad = request.form.get('ciudad')

        exito, mensaje = servicio.actualizar_almacen(id, nombre, pais, ciudad)

        if exito:
            return redirect(url_for('almacenes.almacenes'))
        else:
            return render_template('editar_almacen.html', a=almacen, error=mensaje)

    return render_template('editar_almacen.html', a=almacen)


@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_almacen(id):
    """Elimina el almacen indicado y redirige a la lista."""
    servicio.eliminar_almacen(id)
    return redirect(url_for('almacenes.almacenes'))
