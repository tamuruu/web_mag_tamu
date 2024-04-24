import os

from flask import Blueprint, current_app,render_template, url_for
from flask_login import current_user

from .data import db_session
from .data.add_product import AddProduct
from .data.categories import Categories
from .data.categories_products import Categories_Products

catalog = Blueprint('catalog', __name__)


@catalog.route('catalog/<category>')
def show_catalog(category):
    db_sess = db_session.create_session()
    catalog = db_sess.query(Categories).all()
    catalog_list = {}
    for i in catalog:
        catalog_list[i.name] = i.address
    category = db_sess.query(Categories).filter(Categories.address == category).first()
    id_category = category.id
    category_name = category.name
    products = db_sess.query(Categories_Products).filter(Categories_Products.categori_id == id_category).all()
    spi = []
    for product in products:
        product_text = db_sess.query(AddProduct).filter(AddProduct.id == product.product_id).first()

        image_file1 = url_for('static', filename=f'products_img/{product_text.id}/{product_text.image1}')
        image_file2 = url_for('static', filename=f'products_img/{product_text.id}/{product_text.image2}')
        image_file3 = url_for('static', filename=f'products_img/{product_text.id}/{product_text.image3}')

        spi.append([product_text.id, product_text.name, product_text.price, product_text.discount, product_text.stock,
                    product_text.description, image_file1, True])
    return render_template('catalog.html', user=current_user, sp=spi, catalog_list=catalog_list, category_name=category_name)
