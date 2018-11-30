from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from flask import current_app
from flask_login import login_required


index = Blueprint('index', __name__, template_folder='templates')
@index.route('/')
@login_required
def show():
    print current_app.connector
    return render_template('index/index.html')
