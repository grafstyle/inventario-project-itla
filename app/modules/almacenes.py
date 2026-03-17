from flask import Blueprint, render_template, request, redirect, url_for
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db'))
import database as db
import logic as lg

bp = Blueprint('almacenes', __name__, url_prefix='/almacenes')

@bp.route('')
def almacenes():
    lista = db.get_all_warehouses()
    return render_template('almacenes.html', almacenes=lista)

@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_almacen():
    if request.method == 'POST':
        name    = request.form.get('name')
        country = request.form.get('country')
        city    = request.form.get('city')

        ok, msg = lg.logic_create_warehouse(name, country, city)

        if ok:
            return redirect(url_for('almacenes.almacenes'))
        else:
            return render_template('nuevo_almacen.html', error=msg)

    return render_template('nuevo_almacen.html')

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_almacen(id):
    almacen = db.get_warehouse(id)
    if not almacen:
        return redirect(url_for('almacenes.almacenes'))

    if request.method == 'POST':
        name    = request.form.get('name')
        country = request.form.get('country')
        city    = request.form.get('city')

        ok, msg = lg.logic_update_warehouse(id, name, country, city)

        if ok:
            return redirect(url_for('almacenes.almacenes'))
        else:
            return render_template('editar_almacen.html', almacen=almacen, error=msg)

    return render_template('editar_almacen.html', almacen=almacen)

@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_almacen(id):
    lg.logic_delete_warehouse(id)
    return redirect(url_for('almacenes.almacenes'))
