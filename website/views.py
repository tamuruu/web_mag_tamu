from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
import os
import sqlite3
from .data import db_session
from .data.add_product import AddProduct


views = Blueprint('views', __name__)


@views.route('/')
def home():
    db_sess = db_session.create_session()
    text = db_sess.query(AddProduct).all()
    spi = []
    for i in text:
        files = []
        di = os.path.join(current_app.root_path, 'static', 'products_img', f'{i.id}')
        files += os.listdir(di)
        spi.append([i.id, i.name, i.price, i.discount, i.stock, i.description, files, True])

    return render_template('home.html', user=current_user, sp=spi)
