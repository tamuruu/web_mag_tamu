from flask import Blueprint, render_template, current_app, url_for
from flask_login import login_required, current_user
import os
import sqlite3
from .data import db_session
from .data.add_product import AddProduct
from .data.categories import Categories



views = Blueprint('views', __name__)

@views.route('/')
def home():
    # секции в каталоге
    db_sess = db_session.create_session()
    catalog = db_sess.query(Categories).all()
    catalog_list = {}
    for i in catalog:
        catalog_list[i.name] = i.address

    # отображение картинки в карточку
    text = db_sess.query(AddProduct).all()
    spi = []
    for i in text:
        image_file1 = url_for('static', filename=f'products_img/{i.id}/{i.image1}')
        image_file2 = url_for('static', filename=f'products_img/{i.id}/{i.image2}')
        image_file3 = url_for('static', filename=f'products_img/{i.id}/{i.image3}')

        spi.append([i.id, i.name, i.price, i.discount, i.stock, i.description, image_file1, True])

    return render_template('home.html', user=current_user, sp=spi, catalog_list=catalog_list)
