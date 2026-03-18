from flask import Blueprint, render_template

bp = Blueprint('principal', __name__)

@bp.route('/')
def indice():
    return render_template('hub.html')
