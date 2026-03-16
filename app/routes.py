from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('hub.html')
    
@bp.route('/productos') 
def productos():
    return render_template('productos.html')


