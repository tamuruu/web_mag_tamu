from flask import Blueprint, url_for, render_template, redirect, request
from flask_login import current_user, login_required

from .data import db_session
from .data.add_product import AddProduct
from .data.cart import Cart
from .data.categories import Categories
from .data.favourites import Favourites

fav = Blueprint('fav', __name__)


@login_required
@fav.route('/favourites')
def show_catalog():
    db_sess = db_session.create_session()
    catalog = db_sess.query(Categories).all()
    catalog_list = {}
    for i in catalog:
        catalog_list[i.name] = i.address

    cart = db_sess.query(Cart).filter(Cart.user_id == current_user.id).all()
    cart_list = []
    for i in cart:
        cart_list.append(i.product_id)

    fav = db_sess.query(Favourites).filter(Favourites.user_id == current_user.id).all()
    fav_list = []
    spi = []
    for i in fav:
        fav_list.append(i.product_id)
        product_id = i.product_id
        product = db_sess.query(AddProduct).filter(AddProduct.id == product_id).first()
        image_file1 = url_for('static', filename=f'products_img/{product.id}/{product.image1}')
        image_file2 = url_for('static', filename=f'products_img/{product.id}/{product.image2}')
        image_file3 = url_for('static', filename=f'products_img/{product.id}/{product.image3}')
        spi.append(
            [product.id, product.name, product.price, product.discount, product.stock, product.description, image_file1,
             True])

    return render_template('favourites.html', user=current_user, sp=spi, catalog_list=catalog_list, cart_list=cart_list,
                           fav_list=fav_list)


@login_required
@fav.route('/fav/add/<product_id>')
def add(product_id):
    db_sess = db_session.create_session()
    new_fav = Favourites()
    new_fav.product_id = product_id
    new_fav.user_id = current_user.id
    db_sess.add(new_fav)
    db_sess.commit()
    return redirect(request.referrer)


@login_required
@fav.route('/fav/delete/<product_id>')
def delete(product_id):
    db_sess = db_session.create_session()
    fav = db_sess.query(Favourites).filter(
        Favourites.user_id == current_user.id and Favourites.product_id == product_id).first()
    db_sess.delete(fav)
    db_sess.commit()
    return redirect(url_for('views.home'))
