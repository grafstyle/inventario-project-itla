from flask import Blueprint, render_template, request, redirect, url_for
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'db'))
import database as db
import logic as lg

bp = Blueprint('main', __name__)

db.init_db()

@bp.route('/')
def index():
    return render_template('hub.html')