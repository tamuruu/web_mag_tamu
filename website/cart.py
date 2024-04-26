from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required

from .data.add_product import AddProduct
from .data.cart import Cart
from .data.db_session import create_session

cart = Blueprint('cart', __name__)

@login_required
@cart.route('/cart')
def show_cart():
    db_sess = create_session()
    cart = db_sess.query(Cart).filter(Cart.user_id == current_user.id).all()
    cart_amount = 0
    full_amount = 0
    items = []
    for i in cart:
        cart_amount += i.amount
        product_id = i.product_id
        product = db_sess.query(AddProduct).filter(AddProduct.id == product_id).first()
        image_file1 = url_for('static', filename=f'products_img/{product.id}/{product.image1}')
        items.append([product.id, product.name, product.price, product.discount, i.amount, image_file1])
        full_amount += product.price * (100 - product.discount) / 100 * i.amount

    return render_template('cart.html', amount=cart_amount, items=items, full_amount=full_amount)


@login_required
@cart.route('/cart/add/<product_id>')
def add_product(product_id):
    db_sess = create_session()
    new_product = Cart()
    new_product.user_id = current_user.id
    new_product.product_id = int(product_id)
    new_product.amount = 1
    db_sess.add(new_product)
    db_sess.commit()

    return redirect(request.referrer)


# функция, которая прибавляет еще один товар в корзине
@login_required
@cart.route('/cart/plus_one/<int:product_id>')
def plus_one(product_id):
    db_sess = create_session()
    cart = db_sess.query(Cart).filter(Cart.product_id == product_id and Cart.user_id == current_user.id).first()
    cart.amount = cart.amount + 1
    db_sess.commit()
    return redirect('/cart')


# функция, которая отнимает товар в корзине

@login_required
@cart.route('/cart/minus_one/<int:product_id>')
def minus_one(product_id):
    db_sess = create_session()
    cart = db_sess.query(Cart).filter(Cart.product_id == product_id and Cart.user_id == current_user.id).first()
    cart.amount = cart.amount - 1
    if cart.amount == 0:
        db_sess.delete(cart)
    db_sess.commit()
    return redirect('/cart')
