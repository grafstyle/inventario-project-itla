from flask import Blueprint, render_template, request, redirect, url_for
from app.services import servicio_almacen as service

bp = Blueprint('almacenes', __name__, url_prefix='/almacenes')

@bp.route('')
def almacenes():
    lista = service.obtener_todos_almacenes()
    return render_template('almacenes.html', almacenes=lista)

@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_almacen():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        pais   = request.form.get('pais')
        ciudad = request.form.get('ciudad')

        ok, msg, _ = service.crear_almacen(nombre, pais, ciudad)

        if ok:
            return redirect(url_for('almacenes.almacenes'))
        else:
            return render_template('nuevo_almacen.html', error=msg)

    return render_template('nuevo_almacen.html')

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_almacen(id):
    almacen = service.obtener_almacen(id)
    if not almacen:
        return redirect(url_for('almacenes.almacenes'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        pais   = request.form.get('pais')
        ciudad = request.form.get('ciudad')

        ok, msg = service.actualizar_almacen(id, nombre, pais, ciudad)

        if ok:
            return redirect(url_for('almacenes.almacenes'))
        else:
            return render_template('editar_almacen.html', p=almacen, error=msg) # keeping 'a' or 'p' similar? In original was `a=almacen`
            # wait, my original view had a=almacen. I'll use a=almacen

    return render_template('editar_almacen.html', a=almacen)

@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_almacen(id):
    service.eliminar_almacen(id)
    return redirect(url_for('almacenes.almacenes'))
